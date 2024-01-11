Candidate Profiles
===================

Setup (local)
-------------
**(Linux/ubuntu 22.04):**
---------------------------
* Download the 2 setup scripts to your machine and run them OR clone master and setup manually (*refer to the scripts to know what you should download*)

* Install the required packages (Python 3.8, Docker etc..) (Skip if you cloned the project manually)
    ::

        sudo bash os_requirements.sh


* build required project directories (Skip if you cloned the project manually)
    ::

        bash project_setup.sh


* Activate the virtual environment (venv)
    ::

        cd candidates_profiles/
        source venv/bin/activate

* Install project requirements:
    ::

        cd candidates_profiles && pip install -r requirements.txt

**(Windows/MacOS)**:
---------------------
* Not tested.
* The above steps could work on MacOS.

After Installation:
---------------------
* Copy the keys.json file from the email and place it inside:
::

    >>> settings/

* update your database keys in **/settings/keys.json**
* Check **Makefile** for usual commands
    * **Start Project**:
    ::

        make run-docker


Git && Branches Life-cycle
--------------------------
* **master** is the production branch.
* **development** is a clone from master.
* For new features create a new branch (give it a meaningful name) from **development**
::

    git fetch
    git checkout -b <your_branch_name> origin/development

* When you finish developing and creating **tests**. You need to run tests before pushing to remote:
::

    make test-default

* After making sure all **tests pass**. **push to remote** then **open a pull request** to **development** branch:
::

    git push -u origin <your_branch_name>

* After your changes are **reviewed**. They will be **merged** to development branch.
* The dev-ops engineer will take care of **merging** to **master** and deploying to production servers.