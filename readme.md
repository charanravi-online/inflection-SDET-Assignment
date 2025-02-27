# Instructions

1. clone the repo 

    ```
    git clone https://github.com/charanravi-online/inflection-SDET-Assignment.git
    ```
2. change dir into the repo
    ```
    cd inflection-SDET-Assignment/
    ```
3. run setup.ps1 to create a virtual environment & install requirements.
    ```
    .\setup.ps1
    ```
4. run run.ps1 to run the tests.
    ```
    .\run.ps1
    ```

## NOTES
- Try to run the ps1 files in the poweshell where it's the most compatible. Running it on Command prompt may cause some issues.
- Ensure Docker Desktop is running before executing setup.ps1.
- Stop Docker services after testing with docker-compose -f docker-compose-e2e.yml down.
- If you encounter issues, verify Python 3.11.1+, Docker Compose, and PowerShell execution policy are correctly configured.
- Note that docker-compose-integrations.yml is not used due to unresolved issues.