# Paper discovery resource list

A living catalog of where to find papers, get metadata, download lawful full text, or learn about a topic. Sources are grouped by their primary use. **Adapter candidate** means planned, not implemented; **manual reference** means no automated retrieval is planned for now. Links and general coverage checked 2026-11-21.

## Preprints and full-text downloads

| Provider ID | Site and access route | Use and limits |
|---|---|---|
| `arxiv` | [arXiv](https://arxiv.org/) · [API manual](https://info.arxiv.org/help/api/user-manual.html) | **First adapter.** Find preprints by topic or category and return their abstract and PDF links. Preserve the version when needed; an arXiv posting is not proof of venue acceptance. |

## Citations, references, and metadata

| Provider ID | Site and access route | Use and limits |
|---|---|---|
| `openalex` | [OpenAlex](https://openalex.org/) · [API docs](https://help.openalex.org/api/) · [Pricing](https://help.openalex.org/access/pricing/) | **Adapter candidate.** Look up citation counts, outgoing references, DOI, and open-access locations when available. Record when a count was observed. Single-record lookups are free; search uses a quota. An indexed location is not a guarantee of full-text access. |

## Official proceedings and venue records

| Provider ID | Site and access route | Use and limits |
|---|---|---|
| `acl_anthology` | [ACL Anthology](https://aclanthology.org/) | **Adapter candidate.** Browse NLP proceedings by venue and year, including ACL, EMNLP, and NAACL. Return official paper pages and Anthology PDFs where provided. |
| `cvf_open_access` | [CVF Open Access](https://openaccess.thecvf.com/) | **Adapter candidate.** Find CVPR, ICCV, and other listed computer-vision proceedings, with camera-ready PDFs and supplementary files when available. |
| `openreview` | [OpenReview](https://openreview.net/) · [API documentation](https://docs.openreview.net/) | **Adapter candidate.** Find public venue submissions, decisions, reviews, and PDFs where available. Do not equate a public submission with acceptance. |

## Community trends

| Provider ID | Site and access route | Use and limits |
|---|---|---|
| `huggingface_papers` | [Hugging Face Daily Papers](https://huggingface.co/papers) · [Trending Papers](https://huggingface.co/papers/trending) | **Adapter candidate.** Find papers receiving community attention. Label Daily versus Trending and retain the date or visible signal. Placement and upvotes are not citations or measures of technical quality. Follow the paper link for the original. |

## Tutorials and learning resources

| Site | Use and limits |
|---|---|
| [Dive into Deep Learning](https://d2l.ai/) | **Manual reference.** Build background with explanations, math, and runnable examples. Follow references to find the original work; don't treat tutorial results as results from the paper. |

## Blogs and research commentary

| Site | Use and limits |
|---|---|
| [Google Research Blog](https://research.google/blog/) | **Manual reference.** Find lab announcements and author explanations; follow linked papers to verify technical claims or locate the full text. |

To add a site, record its primary category, canonical URL, official API or feed documentation if available, what it can return, access limits, and when it was checked. Identify which claims or signals still need verification against a paper or official venue record. Configure implemented adapters separately; do not store credentials or downloaded files here.
