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
| `dblp` | [DBLP](https://dblp.org/) | **Manual reference.** Browse conference papers by year and follow DOI or publisher links. Use it as a bibliography, not a PDF host or citation-count provider. |

## Official proceedings and venue records

| Provider ID | Site and access route | Use and limits |
|---|---|---|
| `acl_anthology` | [ACL proceedings](https://aclanthology.org/venues/acl/) · [EMNLP proceedings](https://aclanthology.org/venues/emnlp/) · [NAACL proceedings](https://aclanthology.org/venues/naacl/) | **Adapter candidate.** Pick a year, then open the main proceedings or Long/Short Papers volumes. Findings, demos, and workshops are listed separately where available. Open a paper's entry for its PDF. |
| `cvf_open_access` | [CVPR 2026 papers](https://openaccess.thecvf.com/CVPR2026) · [ICCV 2025 papers](https://openaccess.thecvf.com/ICCV2025) · [CVF archive by year](https://openaccess.thecvf.com/menu) | **Adapter candidate.** Browse CVPR and ICCV paper lists. Open a paper entry for its PDF and supplementary files where available. |
| `ecva` | [ECCV 2026 paper browser](https://eccv.ecva.net/virtual/2026/papers.html) · [ECVA open-access ECCV papers](https://www.ecva.net/papers.php) | **Adapter candidate.** Use the ECCV conference browser for 2026 and the separate ECVA archive for available open PDFs and supplements. |
| `openreview` | [OpenReview](https://openreview.net/) · [API documentation](https://docs.openreview.net/) | **Adapter candidate.** Find public venue submissions, decisions, reviews, and PDFs where available. Do not equate a public submission with acceptance. |
| `acm_dl` | [ACM Digital Library](https://dl.acm.org/) · [ACM proceedings policy](https://www.acm.org/publications/proceedings) | **Adapter candidate.** Publisher records, DOIs, and PDF links for the ACM venues below. Conference programs help identify the correct year and track; some graphics technical papers are published in *ACM Transactions on Graphics* (TOG), not the separate conference proceedings. |
| `eurographics_diglib` | [Eurographics Digital Library](https://diglib.eg.org/) · [Computer Graphics Forum](https://diglib.eg.org/handle/10.2312/1) | **Adapter candidate.** Browse Eurographics collections and follow item pages for available PDFs. Some *Computer Graphics Forum* full texts have access restrictions. |

### Conference labels: examples, not exhaustive coverage

No single page supplies every label. Use proceedings volumes for **publication track** (main proceedings vs. Findings) and **paper length** (Long/Short when stated), the official schedule or paper page for **presentation format** (Oral, Poster, etc.), and official announcements or selections for **recognition** (Best Paper, Highlight, etc.). These are independent: a Long Paper can appear in Findings, and a Best Paper can have both an Oral and a Poster session.

| Venue edition | What these pages can verify |
|---|---|
| **CVPR 2026** | [Best Paper announcement](https://cvpr.thecvf.com/Conferences/2026/News/Best_Papers) and [Highlighted Papers](https://cvpr.thecvf.com/virtual/2026/events/Highlights2026) verify named recognition; the [paper program](https://cvpr.thecvf.com/virtual/2026/papers.html) can show presentation format. |
| **ICCV 2025** | [Awards and highlights](https://iccv.thecvf.com/virtual/2025/awards_detail) shows each listed paper's specific recognition; the [paper program](https://iccv.thecvf.com/virtual/2025/papers.html) can show presentation format. An entry on the awards page is not necessarily a Best Paper winner. |
| **ECCV 2026** | [Awards](https://eccv.ecva.net/virtual/2026/awards_detail) identifies named recognition; the [paper program](https://eccv.ecva.net/virtual/2026/papers.html) can show presentation format. |
| **ACL 2026, EMNLP 2026, NAACL 2025** | Use the Anthology venue links above to inspect main proceedings volumes; compare the separate Findings volumes for [ACL](https://aclanthology.org/volumes/2026.findings-acl/), [EMNLP](https://aclanthology.org/volumes/2026.findings-emnlp/), and [NAACL](https://aclanthology.org/volumes/2025.findings-naacl/). For recognition, see the official [ACL](https://2026.aclweb.org/program/best_papers/), [EMNLP](https://2026.emnlp.org/program/awards/), and [NAACL](https://2025.naacl.org/blog/best-papers/) award pages. Check the matching year's schedule for Oral or Poster. |

Coverage and terminology vary by edition. Keep the venue's exact label and a source link for each verified field. Leave unverified fields unknown: absence from an oral list does not prove a paper was a poster, and a Highlight does not imply an Oral.

### Information retrieval and web search

| Venue | Where to find papers |
|---|---|
| **SIGIR** — information retrieval and search | [2026 accepted papers](https://sigir2026.org/en-AU/pages/program/accepted-papers) · [DBLP by year](https://dblp.org/db/conf/sigir/) |
| **WSDM** — web search and data mining | [Conference series archive](https://www.wsdm-conference.org/) · [2026 accepted papers](https://wsdm-conference.org/2026/index.php/accepted-papers/) · [DBLP by year](https://dblp.org/db/conf/wsdm/) |
| **CIKM** — information and knowledge management, including retrieval | [2025 accepted papers](https://www.cikm2025.org/program/accepted-papers) · [DBLP by year](https://dblp.org/db/conf/cikm/) |
| **ICTIR** — information retrieval theory | [2026 program with paper DOIs](https://sigir-ictir.github.io/ictir2026/program/) · [DBLP by year](https://dblp.org/db/conf/ictir/) |
| **The Web Conference (WWW)** — broader web research, including search | [2026 conference site](https://www2026.thewebconf.org/) · [2026 main proceedings](https://dl.acm.org/doi/proceedings/10.1145/3774904) · [DBLP by year](https://dblp.org/db/conf/www/) |

### Computer graphics

| Venue | Where to find papers |
|---|---|
| **SIGGRAPH** | [2026 Technical Papers program](https://s2026.siggraph.org/program/technical-papers/) · [DBLP by year](https://dblp.org/db/conf/siggraph/) |
| **SIGGRAPH Asia** | [2025 proceedings guide](https://asia.siggraph.org/2025/program/conference-proceedings/) · [DBLP by year](https://dblp.org/db/conf/siggraphasia/) |
| **Eurographics** | [2026 conference site](https://eg2026.github.io/) · [Eurographics Digital Library](https://diglib.eg.org/) · [DBLP by year](https://dblp.org/db/conf/eurographics/) |

## Community trends

| Provider ID | Site and access route | Use and limits |
|---|---|---|
| `huggingface_papers` | [Monthly Papers (November 2026)](https://huggingface.co/papers/month/2026-11) · [Daily Papers](https://huggingface.co/papers) · [Trending Papers](https://huggingface.co/papers/trending) | **Adapter candidate.** Use the monthly view to find papers receiving community attention in a calendar month. Change `YYYY-MM` in `/papers/month/YYYY-MM` or use the page arrows. Label the view and month or date, and record visible upvotes separately from citation counts. Follow the paper link for the original. |

## Tutorials and learning resources

| Site | Use and limits |
|---|---|
| [Dive into Deep Learning](https://d2l.ai/) | **Manual reference.** Build background with explanations, math, and runnable examples. Follow references to find the original work; don't treat tutorial results as results from the paper. |

## Blogs and research commentary

| Site | Use and limits |
|---|---|
| [Google Research Blog](https://research.google/blog/) | **Manual reference.** Find lab announcements and author explanations; follow linked papers to verify technical claims or locate the full text. |

To add a site, record its primary category, canonical URL, official API or feed documentation if available, what it can return, access limits, and when it was checked. Identify which claims or signals still need verification against a paper or official venue record. Configure implemented adapters separately; do not store credentials or downloaded files here.
