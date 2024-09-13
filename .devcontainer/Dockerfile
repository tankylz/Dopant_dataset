FROM mcr.microsoft.com/devcontainers/miniconda:1-3

# Install mamba for faster dependency resolution
RUN conda install -n base -c conda-forge mamba

# Copy environment.yml and create the environment
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
# Set the solver to classic to avoid issues with libmamba
RUN conda config --set solver classic
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then \
      umask 0002 && /opt/conda/bin/mamba env create -f /tmp/conda-tmp/environment.yml && \
      echo "Environment 'smol-tester' created successfully" && \
      rm -rf /tmp/conda-tmp; \
    else \
      echo "No environment.yml file found"; \
    fi

# Verify architecture
RUN uname -m

# [Optional] Uncomment to install a different version of Python than the default
# RUN conda install -y python=3.6 \
#     && pip install --no-cache-dir pipx \
#     && pipx reinstall-all

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
