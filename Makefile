##
## EPITECH PROJECT, 2018
## SEC_crypto_2018
## File description:
## Makefile
##

IDS		=	01 02 03 04 05 06 07 08 09 10 11 12

SRCDIR		=	src

NAME		=	$(addprefix challenge,$(IDS))

CP		=	cp
CHMOD_X		=	chmod +x
RM		=	rm -rf

all: $(NAME)

$(NAME): %: $(SRCDIR)/%.py
	$(CP) $< $@
	$(CHMOD_X) $@

clean:

fclean:	clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
