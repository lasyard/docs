PUML_C := java -jar ~/bin/plantuml.jar -failfast2 -tpng

PUML_SRCS := $(wildcard _images/src/*.puml _images/src/*/*.puml)

PUML_PNGS := $(patsubst _images/src/%.puml,_images/generated/%.png,$(PUML_SRCS))

_images/generated/%.png: _images/src/%.puml
	$(PUML_C) $^
	mkdir -p $(@D) && mv -f $(^:%.puml=%.png) $@

.PHONY: puml puml_clean

puml: $(PUML_PNGS)

puml_clean:
	-rm -f $(PUML_PNGS)
