Cloning the repository
======================

To clone the |SDK_project| repository, you can use the Repo tool. The tool is available here: (|git_repo_tool_url|).
Cloning ensures all components and dependencies are fetched and in a suitable default location on the
file system. To initialize the repo structure for the entire |SDK_project|, including all components, run:

.. code-block:: bash

    repo init -u <manifest-url> -g all

After the repo is initialized, fetch the contents with:

.. code-block:: bash

    repo sync

.. note::
    You must enable long paths on Windows®. To ensure nested submodules do not exceed the maximum long path
    length, you must clone close to the root directory or use a symlink.

Due to a bug in git-repo, nested submodules do not always update as part of repo sync. Therefore, you need
to manually update nested submodules, for example:

.. code-block:: bash

    cd dependencies/glslang
    git submodule update --init --recursive

After the sync command completes successfully, you can find the individual components in :code:`<repo_root>/sw/`.
You can also find all the required dependencies in :code:`<repo_root>/dependencies/`.

.. tip::
    You can initialize the repo with only the components you need. This also fetches only the dependencies
    required by the selected components. The :code:`-g all` in the preceding initialization command is equivalent
    to :code:`-g model-converter vgf-lib scenario-runner emulation-layer`. Some components may also force other components
    to be included. For example, :code:`scenario-runner` automatically includes :code:`vgf-lib` because :code:`vgf-lib`
    is required.

.. hint::
    Although not recommended, it is possible to check out the components using :code:`git clone` commands directly.
    This requires checking out each component and dependency manually. The custom location to each dependency needs
    to be configured explicitly by options to the build command for each component which results in a more complicated
    workflow.
