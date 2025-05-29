DRAWIO_C := /Applications/draw.io.app/Contents/MacOS/draw.io -x -f png

DRAWIO_SRCS := $(wildcard _images/src/*.drawio _images/src/*/*.drawio _images/src/*/*/*.drawio)

DRAWIO_PNGS := $(patsubst _images/src/%.drawio,_images/generated/%.png,$(DRAWIO_SRCS))

_images/generated/%.png: _images/src/%.drawio
	- mkdir -p $(@D)
	$(DRAWIO_C) -o $@ $^

.PHONY: drawio drawio_clean

drawio: $(DRAWIO_PNGS)

drawio_clean:
	-rm -f $(DRAWIO_PNGS)
