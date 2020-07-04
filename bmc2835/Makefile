.PHONY: all clean

OBJECTS = led-on.img blink.img

all: $(OBJECTS)

clean:
	rm -vf $(OBJECTS)

%.img: %.elf
	arm-none-eabi-objcopy $< -O binary $@

%.elf: %.o
	arm-none-eabi-ld --no-undefined $< -o $@ -T kernel.ld

%.o: %.s
	arm-none-eabi-as $*.s -o $*.o
