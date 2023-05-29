
SILENCE = @

# target file naming

TARGET_LIB=$(OBJS_DIR)/libvideobuf.a

PROJECT_ROOT = ..


# CFLAG CONFIG
# DEBUG/SMALLEST/FASTEST
OPTIMIZE_LEVEL = SMALLEST
STRICT_WARNING = Y
USE_SMALL_DATA = N
USE_LARGE_MEMORY_MODEL = Y

# Source files
SRC_DIR = ./




# Header files
INC_DIR   = $(PROJECT_ROOT)/inc/






INSTALL_DIR = $(PROJECT_ROOT)/lib
OBJS_DIR = objs

ARC_CROSS_COMPILE?=arc-fullhan-elf32-
CC=${ARC_CROSS_COMPILE}gcc
AR=${ARC_CROSS_COMPILE}ar
OBJCOPY=${ARC_CROSS_COMPILE}objcopy
OBJDUMP=${ARC_CROSS_COMPILE}objdump

CFLAGS = -marc600 -Werror  -ffunction-sections

# PREDEFINED MACRO
# optimize level: DEBUG/SMALLEST/FASTEST
ifndef OPTIMIZE_LEVEL
	OPTIMIZE_LEVEL = SMALLEST
endif

ifndef STRICT_WARNING
	STRICT_WARNING = N
endif

ifndef USE_SMALL_DATA
	USE_SMALL_DATA = Y
endif

ifndef USE_LARGE_MEMORY_MODEL
	USE_LARGE_MEMORY_MODEL = Y
endif

# CFLAG CONFIG
# optimize level
ifeq ($(OPTIMIZE_LEVEL), DEBUG)
	CFLAGS += -O0
endif

ifeq ($(OPTIMIZE_LEVEL), SMALLEST)
	CFLAGS += -Os -mno-millicode
endif

ifeq ($(OPTIMIZE_LEVEL), FASTEST)
	CFLAGS += -O2
endif

# strict warning treat warning as error
ifeq ($(STRICT_WARNING), Y)
	CFLAGS += -Werror
endif

# disable small data register
ifeq ($(USE_SMALL_DATA), N)
	CFLAGS += -mno-sdata
endif

# memory model
ifeq ($(USE_LARGE_MEMORY_MODEL), Y)
	CFLAGS += -mlong-calls
endif

DEP_FLAGS= -MMD -MP

# some path abbreviations




INC_DIR ?= ./
INC_DIR  = $(PROJECT_ROOT)/inc/
INC_DIR  += $(PROJECT_ROOT)/inc/driver
INC_DIR  += $(PROJECT_ROOT)/inc/ctrl
INC_DIR  += $(PROJECT_ROOT)/TOSD/
INC_DIR  += $(PROJECT_ROOT)/libc/
INC_DIR  += $(PROJECT_ROOT)/ext/
INC_DIR  += $(PROJECT_ROOT)/video_buf/



# INC_DIR  += $(PROJECT_ROOT)/platform/chip

# Header files
HEADER_FILE=$(foreach file,$(INC_DIR),$(addprefix -I,$(file)))

# Source files
SRC_FILE=$(foreach file,$(SRC_DIR),$(addprefix $(file),*.c))

# object file lists
CSRC_FILES = $(wildcard $(SRC_FILE))
COBJ_FILES = $(addprefix $(OBJS_DIR)/, $(CSRC_FILES:.c=.o))

# Dependent files
DEP_FILES = $(addprefix $(OBJS_DIR)/, $(CSRC_FILES:.c=.d))

# STUFF_TO_CLEAN
STUFF_TO_CLEAN += $(DEP_FILES) $(COBJ_FILES)
STUFF_TO_CLEAN += $(TARGET_LIB)
# add include files for compile flags
CFLAGS   += $(HEADER_FILE)

.PHONY: all
all: $(TARGET_LIB)
	$(SILENCE) mkdir -p $(INSTALL_DIR)
#	@echo Installing target to $(INSTALL_DIR)
	$(SILENCE)cp $(TARGET_LIB) $(INSTALL_DIR)/.

$(TARGET_LIB): $(COBJ_FILES)
	@echo Building target $(notdir $@)
	$(SILENCE) $(AR) -rcs $@ $^


$(OBJS_DIR)/%.o:%.c
	@echo Compiling $(notdir $@)
	$(SILENCE) mkdir -p $(dir $@)
	$(SILENCE) $(CC) $(DEP_FLAGS) $(CFLAGS) -o $@ -c $<

-include $(DEP_FILES)

.PHONY: clean
clean:
#	@echo Cleaning...
	$(SILENCE) rm -rf $(OBJS_DIR)
	$(SILENCE) rm -f $(STUFF_TO_CLEAN)
