# Anvur Journal download and parsing

## Notes
As of 2023-10-29 there is an issue with tabula_py being based on an outdated PyPDF2 API version, and new PyPDF API have a breaking change.  
Short term fix is to manually install an older PyPDF2 version with `python -m pip install "pypdf2<3"` before loading tabula_py.
