MAIN := main
BUILD := build
MANAGED_TEXLIVE_BIN := $(dir $(firstword $(wildcard $(HOME)/.cache/codex-runtimes/codex-texlive/full/bin/*/latexmk)))

ifneq ($(MANAGED_TEXLIVE_BIN),)
export PATH := $(MANAGED_TEXLIVE_BIN):$(PATH)
endif

.PHONY: pdf clean

pdf:
	@mkdir -p $(BUILD)
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 -outdir=$(BUILD) $(MAIN).tex; \
	elif command -v tectonic >/dev/null 2>&1; then \
		tectonic -X compile $(MAIN).tex --outdir $(BUILD); \
	else \
		echo "没有找到 LaTeX 编译器。请安装 MacTeX、BasicTeX 或 Tectonic。"; \
		exit 1; \
	fi

clean:
	@rm -rf $(BUILD)
