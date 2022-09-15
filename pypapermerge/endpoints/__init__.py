"""
All (implemented) endpoint modules of the papermerge API

## Currently implemented

- [ ] auth
    * [x] login
- [ ] documents
    * [x] document_list
    * [x] upload file
    * [x] delete documents
- [ ] nodes
    * [x] nodes_create
- [ ] folders
- [ ] groups
- [ ] ocr
- [ ] pages
- [ ] permissions
- [ ] preferences
- [ ] schema
- [ ] search
- [ ] tags
- [ ] tokens
- [ ] users
- [ ] version

"""
from .documents import Documents
from .nodes import Nodes
