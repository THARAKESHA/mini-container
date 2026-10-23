CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=gnu99
LDFLAGS = -pthread -lrt

SRC_DIR = src
TEST_DIR = tests
BIN = minicontainer

SRCS = $(SRC_DIR)/main.c $(SRC_DIR)/namespaces.c $(SRC_DIR)/cgroups.c
OBJS = $(SRCS:.c=.o)

TEST_SRCS = $(wildcard $(TEST_DIR)/*.c)
TEST_BINS = $(TEST_SRCS:.c=)

.PHONY: all clean rootfs test demo menu monitor

all: $(BIN) $(TEST_BINS)

$(BIN): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(TEST_DIR)/%: $(TEST_DIR)/%.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

rootfs:
	bash scripts/setup_rootfs.sh

demo: all rootfs
	sudo bash scripts/run_demo.sh

menu: all rootfs
	sudo bash interactive_menu.sh

monitor: all
	sudo bash scripts/monitor.sh

clean:
	rm -f $(BIN) $(OBJS) $(TEST_BINS)
