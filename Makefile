##
## EPITECH PROJECT, 2018
## SEC_crypto_2018
## File description:
## Makefile
##

IDS		=	01 02 03 04 05 06 07 08 09

SRCDIR		=	src
DISTDIR		=	dist

NAME		=	$(addprefix challenge,$(IDS))

CP		=	cp
RM		=	rm -rf

all: $(NAME)

$(NAME): challenge%: $(DISTDIR)/challenge%
	$(CP) $< $@

clean:

fclean:	clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
