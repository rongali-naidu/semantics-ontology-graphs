# 3. Where semantic models live: repositories and model-as-code

A semantic model is a set of definitions: tables, joins, measures,
hierarchies, security. Every BI tool has to **store** those definitions
somewhere and **promote** them from development to production. In BI,
"repository" means two different things:

| | **Metadata repository** (tool-managed) | **Source repository** (user-defined, git) |
|---|---|---|
| What | A database or binary file *inside* the BI platform holding the model | A git repo *you* own (GitHub, GitLab, Azure DevOps, Bitbucket) holding the model as text files |
| Examples | Oracle BI RPD, BusinessObjects CMS, MicroStrategy metadata, Cognos Content Store, Tableau repository, Qlik Repository Service | Oracle Analytics Semantic Modeler (SMML), Power BI projects (PBIP/TMDL), LookML, dbt, Cube, AtScale SML, ThoughtSpot TML, Apache Ossie |
| Diff / review | hard (binary or opaque) | line-by-line diffs, pull requests |
| Parallel development | check-out/lock or special merge tools | branches + merges |
| CI/CD | vendor promotion tools | pipelines, validators, automated deploys |

The industry has been moving from the left column to the right: **semantic
model as code**, stored in a repository the customer controls, with the BI
service acting as the *runtime* that the repository is deployed to.

```
   developer ──edit──► git repo (your branch) ──PR/review──► main ──deploy──► BI service (runtime)
     │                     │                                   │                 │
   desktop / web IDE    text model files                   CI: validate,     dev → test → prod
   (Desktop, Modeler,   (TMDL, SMML, LookML,               lint, test        workspaces / instances
    Looker IDE)          YAML)
```

---

## 3.1 Oracle Analytics (OAC / OAS, formerly OBIEE)

Oracle's semantic model has always been called **the repository**.

### Classic: the RPD file

* A single **`.rpd`** file (binary, password-protected) loaded by the BI
  Server. It has **three layers**:

  | Layer | Contains | Retail example |
  |---|---|---|
  | **Physical** | connection pools, physical tables, keys, joins | `retail.order_lines`, `retail.orders`, ... with FK joins |
  | **Business Model and Mapping (BMM)** | logical tables (facts/dimensions), logical columns, aggregation rules, logical joins, dimension hierarchies, level-based measures | logical fact *Order Lines* with `Revenue = SUM(quantity * unit_price)`; logical dimensions *Customer*, *Product* with a *Department → Product* hierarchy |
  | **Presentation** | subject areas, presentation tables/columns that users see | subject area *Retail Orders* |

* Edited with the **Model Administration Tool / BI Administration Tool**
  (Windows client), either *offline* (edit the file, then upload) or *online*
  (connected to the running BI Server).
* Deployed to OAC by uploading/replacing the data model (console snapshot or
  `datamodel` command-line utility); on OAS via the console or Enterprise
  Manager.
* **Team development** without git: **MUDE** (Multi-User Development
  Environment) with a master RPD on a shared drive, projects checked out,
  then merged back. The tool also does three-way **compare / merge** and
  XML **patch** files (`biserverxmlgen` / `biserverxmlexec`).
* **Source control** for the RPD: save it as **MDS XML** (one XML file per
  object), so it can be committed to git or SVN and diffed.

### Modern: Semantic Modeler + your Git repository

* **Semantic Modeler** (web-based, in OAC) defines the same three layers but
  stores them as **SMML** (Semantic Model Markup Language, JSON) files.
* It **integrates with a Git repository you define** (e.g. GitHub, GitLab):
  initialise the semantic model against the repo, work on branches, commit,
  push/pull and merge from the Modeler UI, and keep the full history in your
  own repository.
* When ready, you **deploy** the semantic model to make it the live model
  for that OAC instance; other instances (test/prod) deploy from the same repo.
* Existing RPDs can be brought into Semantic Modeler (check Oracle's docs for
  the current migration path).

| Concept | RPD (classic) | Semantic Modeler |
|---|---|---|
| Storage | `.rpd` binary (or MDS XML export) | SMML JSON files |
| Repository | file system / MUDE shared drive | **user-defined Git repo** |
| Editing | Windows admin tool | browser |
| Collaboration | MUDE check-out/merge | git branches, commits, merges |
| Promotion | upload/replace RPD | deploy from git |

Status of an Oracle Analytics example with the retail model: see
[`ROADMAP.md`](../../ROADMAP.md).

---

## 3.2 Microsoft Power BI / Fabric

* **Runtime repository:** the semantic model lives in a **workspace** in
  the Power BI / Fabric service (data in VertiPaq, DirectQuery, or Direct
  Lake over OneLake).
* **Authoring files:**
  * `.pbix`: the classic single binary file (report + model). Not
    diff-friendly.
  * **Power BI Project (`.pbip`)**: saves as a *folder* of text files:

    ```
    Retail.pbip
    Retail.Report/            report definition (PBIR)
    Retail.SemanticModel/
    ├── definition.pbism      semantic-model item settings
    ├── .platform             Fabric git metadata (type, display name, logical id)
    └── definition/           the model in TMDL
        ├── database.tmdl  model.tmdl  expressions.tmdl  relationships.tmdl
        └── tables/*.tmdl
    .gitignore                excludes .pbi/localSettings.json, .pbi/cache.abf
    ```

    The retail model in this repo is laid out exactly like this:
    [`implementations/providers/microsoft/power-bi/Retail.SemanticModel/`](../implementations/providers/microsoft/power-bi/Retail.SemanticModel/).
* **User-defined repository:** **Fabric Git integration** connects a
  workspace to a branch/folder in **Azure DevOps** or **GitHub**. You commit
  workspace changes to git or update the workspace from git; "branch out"
  creates a feature workspace per branch.
* **Promotion:** **deployment pipelines** (dev → test → prod workspaces with
  deployment rules for parameters), or CI/CD using Fabric REST APIs /
  `fabric-cicd`.
* **External tools** connect to the model through the **XMLA endpoint**:
  Tabular Editor (including Best Practice Analyzer rules in CI), SSMS, ALM
  Toolkit (schema compare/merge), DAX Studio.

---

## 3.3 Google Looker

* A **LookML project is a git repository** from the start: Looker-hosted
  bare repo, or your own GitHub / GitLab / Bitbucket / Azure DevOps.
* **Development Mode** gives each developer a personal branch; **Production
  Mode** serves the main branch; *Deploy to Production* merges. You can
  require pull requests and run deploy webhooks.
* Validation: **LookML Validator**, data tests (`test:` blocks), Content
  Validator; CI tools such as Spectacles.
* Retail example: [`implementations/providers/gcp/looker/`](../implementations/providers/gcp/looker/).

## 3.4 Tableau

* **Published data sources** (the reusable model: connections, relationships,
  calculated fields) live on Tableau Server/Cloud, whose internal **Tableau
  repository** (PostgreSQL) and file store hold them. Files are `.tds` (XML)
  or `.tdsx` (packaged with extracts); revision history is kept on the server.
* Promotion: REST API, Tableau Content Migration Tool.
* **Tableau Semantics** (Tableau Next) keeps semantic models as metadata in
  Salesforce Data Cloud.

## 3.5 SAP BusinessObjects and SAP Datasphere

* **Universes** (`.unx`) are designed in the **Information Design Tool** as
  a local project (data foundation `.dfx` + business layer `.blx`) and
  **published to the CMS repository** (Central Management Server database);
  security in the CMC; promotion with **Promotion Management** (LCM). Legacy
  `.unv` universes come from the Universe Design Tool.
* **SAP Datasphere** stores analytic models in its repository; transport
  via packages, with CSN (Core Schema Notation, JSON) for definitions.

## 3.6 IBM Cognos Analytics

* **Framework Manager** models (`.cpf` project + `model.xml`) are
  **published as packages** to the **Content Store** database; web-based
  **data modules** also live in the Content Store. Promotion via deployment
  archives.

## 3.7 MicroStrategy (Strategy)

* Schema objects (attributes, facts, hierarchies) and application objects
  (metrics, filters) live in the **metadata repository** (a database).
  **Object Manager** migrates objects between environments. **Strategy
  Mosaic** exposes the semantic layer to other tools.

## 3.8 Qlik

* The data model and **master items** (governed dimensions/measures) live
  inside the **app** (`.qvf`); on Qlik Sense Enterprise apps are managed by
  the **Qlik Repository Service** (PostgreSQL), on Qlik Cloud in spaces.
  Load scripts can be versioned with third-party git tooling.

## 3.9 ThoughtSpot

* Models / worksheets are exported as **TML** (YAML); **Git integration**
  (GitHub) version-controls TML and deploys it across orgs/environments.

## 3.10 Headless and warehouse-native layers

| Tool | Repository model |
|---|---|
| dbt Semantic Layer | dbt project in your git repo; dbt Cloud/CI builds & deploys ([retail_dbt](../implementations/tools/dbt/retail_dbt/)) |
| Cube | model files in your git repo; Cube Cloud deploys from a branch |
| AtScale | SML files in your git repo; AtScale Design Center can connect to git ([sml](../implementations/tools/atscale/sml/)) |
| Snowflake semantic views | objects in the Snowflake catalog; keep the DDL/YAML in git and deploy with CI (Snowflake CLI, Terraform, schemachange) |
| Databricks metric views | objects in Unity Catalog; keep the YAML/SQL in git and deploy with Databricks Asset Bundles |
| Apache Ossie | plain YAML/JSON documents, meant to live in git and be converted to/from tool formats |

---

## 3.11 Summary

| Tool | Runtime store | Editable text format | User-defined git repo | Promotion |
|---|---|---|---|---|
| Oracle Analytics (classic) | RPD loaded in BI Server | MDS XML export | via MDS XML (manual) | upload / replace RPD |
| **Oracle Analytics Semantic Modeler** | deployed semantic model | **SMML** (JSON) | **built in (Git)** | deploy from Modeler |
| **Power BI / Fabric** | workspace | **TMDL** (PBIP) / TMSL | **Fabric Git integration** (Azure DevOps, GitHub) | deployment pipelines, REST |
| Looker | Looker instance (production branch) | LookML | **built in** | deploy to production |
| Tableau | Tableau repository (Server/Cloud) | `.tds` XML | no (files + REST) | REST, Content Migration Tool |
| SAP BusinessObjects | CMS repository | `.unx` (binary project files) | no | Promotion Management |
| IBM Cognos | Content Store | `model.xml` | no (files) | deployment archives |
| MicroStrategy | metadata repository | — | no | Object Manager |
| Qlik Sense | app / Repository Service | load script | third-party | QMC / APIs |
| ThoughtSpot | ThoughtSpot cluster | TML (YAML) | **built in (GitHub)** | git-based deploy |
| dbt, Cube, AtScale, Ossie | runtime engine | YAML | **native** | CI/CD |

## 3.12 Good practice, whichever tool

1. **Keep the model in a repository you own**, as text. Use the tool's git
   integration if it has one (Semantic Modeler, Fabric, Looker, ThoughtSpot);
   otherwise export to a text format (MDS XML, TMDL, `.tds`) on every change.
2. **Never commit credentials.** Connection details become parameters
   (Power BI `expressions.tmdl`, RPD connection pools set per environment).
3. **One branch per change, review by pull request**, and validate in CI:
   Tabular Editor BPA, LookML Validator, `mf validate-configs`, the Ossie JSON
   schemas (as this repo does).
4. **Separate environments** (dev/test/prod) and promote the *same* files,
   with only parameters differing.
5. **Keep a portable copy**: an Apache Ossie export lets you move or share
   the model across tools, and validate its metrics independently (see
   [`check_semantic_model.py`](../../examples/retail/scripts/check_semantic_model.py)).

Next: [4. Open semantic formats](04-open-semantic-formats.md)
