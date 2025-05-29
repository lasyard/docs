.PHONY: all clean

all: drawio puml
clean: drawio_clean puml_clean

include drawio.mk
include puml.mk
