Cloning the repository
======================

To clone the |SDK_project| repository, you can use the Repo tool. The tool is available here: (|git_repo_tool_url|).
Cloning using Repo tool ensures all components and dependencies are fetched and in a suitable default location on the
file system. To initialize the repo structure for the entire |SDK_project|, including all components, run:

.. code-block:: bash

    repo init -u https://github.com/arm/ai-ml-sdk-manifest.git -g all

After the repository is initialized, fetch the contents with:

.. code-block:: bash

    repo sync

.. admonition:: Note: Cloning on Windows®

    To ensure nested submodules do not exceed the maximum long path length, you must enable long paths on Windows®, and
    you must clone close to the root directory or use a symlink. Make sure to use Git for Windows.

    Using **PowerShell**:

    .. code-block:: powershell

        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
        git config --global core.longpaths true
        git --version # Ensure you are using Git for Windows, for example 2.50.1.windows.1
        git clone <git-repo-tool-url>
        python <path-to-git-repo>\git-repo\repo init -u <manifest-url> -g all
        python <path-to-git-repo>\git-repo\repo sync

    Using **Git Bash**:

    .. code-block:: bash

        cmd.exe "/c reg.exe add \"HKLM\System\CurrentControlSet\Control\FileSystem"" /v LongPathsEnabled /t REG_DWORD /d 1 /f"
        git config --global core.longpaths true
        git --version # Ensure you are using the Git for Windows, for example 2.50.1.windows.1
        git clone <git-repo-tool-url>
        python <path-to-git-repo>/git-repo/repo init -u <manifest-url> -g all
        python <path-to-git-repo>/git-repo/repo sync

Due to a known issue in :code:`git-repo`, nested submodules do not always update as part of :code:`repo sync` and need to
be manually updated, for example:

.. code-block:: bash

    cd dependencies/tosa_mlir_translator
    git submodule update --init --recursive

After the sync command completes successfully, you can find the individual components in :code:`<repo_root>/sw/`.
You can also find all the required dependencies in :code:`<repo_root>/dependencies/`.

.. tip::
    You can initialize the repository with only the components that you need. This also fetches only the dependencies
    required by the selected components. The :code:`-g all` in the preceding initialization command is equivalent
    to :code:`-g model-converter vgf-lib scenario-runner emulation-layer`. Some components may also force other components
    to be included. For example, :code:`scenario-runner` automatically includes :code:`vgf-lib` because :code:`vgf-lib`
    is required.

.. note::
    Although we do not recommend this method, you can check out the components using :code:`git clone` commands directly.
    This requires checking out each component and dependency manually. The custom location to each dependency needs
    to be configured explicitly by options to the build command for each component which results in a more complicated
    workflow.
