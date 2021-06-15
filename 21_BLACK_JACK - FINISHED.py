import random


class RE_21:

    def __init__(self):

        # all cards generated from 1 to 11
        self.deck = [card for card in range(1, 12)]

        # yet noone has folded
        self.player_fold = False
        self.pc_fold = False

        # player's and pc's decks
        self.players_deck = []
        self.pc_deck = []

        # to each deck give at the beginning one random card
        random_card_player = self.draw_card()
        self.players_deck.append(random_card_player)

        random_card_pc = self.draw_card()
        self.pc_deck.append(random_card_pc)

        # first player has its move
        self.player_move()


    def draw_card(self):
        # choose random card from available cards and remove it and make it unavailable, and return that random card
        self.card_drawn = random.choice(self.deck)
        self.deck.remove(self.card_drawn)

        return self.card_drawn


    def print_decks(self):

        # you can see all the pc's cards besides his first
        pc_deck_seen = ['?']

        pc_folded = 'FOLDED' if self.pc_fold else 'NOT FOLDED'
        player_folded = 'FOLDED' if self.player_fold else 'NOT FOLDED'

        for pc_cards in self.pc_deck[1:]:
            pc_deck_seen.append(pc_cards)

        print('')
        print('(' + pc_folded + ") PC's DECK:\n" + str(pc_deck_seen))
        print('SUM: ? +', sum(self.pc_deck[1:]))
        print('')
        print('(' + player_folded + ") YOUR DECK:\n" + str(self.players_deck))
        print('SUM:', sum(self.players_deck))
        print('')


    def player_move(self):

        if not self.player_fold:

            self.print_decks()

            while True:

                print('')
                # ask the player to hit or fold
                self.hit_or_fold = input('Hit or Fold? hit/fold: ').lower()

                if self.hit_or_fold == 'hit':

                    # give him random card from the deck
                    random_card = self.draw_card()
                    self.players_deck.append(random_card)

                    self.print_decks()

                    break

                elif self.hit_or_fold == 'fold':
                    # folded his cards
                    self.player_fold = True
                    break

                else:
                    print('')
                    print('Wrong input, type hit/fold !!!')

            self.print_decks()

            # depends who has folded and who has not, the next turn will occur
            if not self.pc_fold:
                self.pc_move()

            elif self.pc_fold and not self.player_fold:
                self.player_move()

            elif self.pc_fold and self.player_fold:
                # if both have folded decide who is the winner
                self.decide_winner()


        elif self.player_fold:
            self.pc_move()


    def pc_move(self):

        if not self.pc_fold:

            self.print_decks()

            # time to 'decide' for the pc to 'calculate', don't want it to be so fast
            time_to_decide = random.randrange(10_000_000, 60_000_000)
            i = 0

            while i <= time_to_decide:
                i += 1

            else:

                # cards that are impossible to draw
                cards_not_to_draw = []

                for card_in_players_deck in self.players_deck[1:]:
                    cards_not_to_draw.append(card_in_players_deck)
                cards_not_to_draw += self.pc_deck

                # all the possible cards to draw
                possible_cards_to_draw = [self.players_deck[0]]

                for possible_card_to_draw in self.deck:

                    if possible_card_to_draw in cards_not_to_draw:
                        pass
                    else:
                        possible_cards_to_draw.append(possible_card_to_draw)


                # if there is a card which will give player, if hits, more than 21
                possible_more_than_21_for_player = 0

                for possible_more_than_21_for_player_card in possible_cards_to_draw:

                    if sum(self.players_deck[1:]) + possible_more_than_21_for_player_card > 21:
                        possible_more_than_21_for_player += 1

                # calculate the possibility where player could draw a card which will give him more than 21
                possibility_more_than_21_for_player = possible_more_than_21_for_player / len(possible_cards_to_draw) * 100


                # if there is a card which will give pc more than 21
                possible_more_than_21_for_pc = 0

                for possible_more_than_21_for_pc_card in possible_cards_to_draw:

                    if sum(self.pc_deck) + possible_more_than_21_for_pc_card > 21:
                        possible_more_than_21_for_pc += 1

                # possibility where pc could draw a card which will give it more than  21
                possibility_more_than_21_for_pc = possible_more_than_21_for_pc / len(possible_cards_to_draw) * 100


                # depends on the situations and probabilities, the pc will decide whether to fold or hit another card
                if (sum(self.players_deck[1:]) < 21 and sum(self.pc_deck) < 21) and (30 < possibility_more_than_21_for_pc < 85) or \
                    (30 < possibility_more_than_21_for_player < 85):

                    overall_possibility = (possibility_more_than_21_for_player + possibility_more_than_21_for_pc) / 2

                    random_true_and_false = [True for _ in range(int(overall_possibility) // 10)] + [False for _ in range(10 - int(overall_possibility) // 10)]
                    random.shuffle(random_true_and_false)

                    self.pc_fold = random.choice(random_true_and_false)

                elif sum(self.players_deck[1:]) >= 21 or sum(self.pc_deck) >= 21:
                    self.pc_fold = True

                elif possibility_more_than_21_for_pc >= 85 or possibility_more_than_21_for_player >= 85:
                    self.pc_fold = True

                else:
                    self.pc_fold = False


                self.print_decks()


                # depends on who has folded and not playing, the next turn will occur
                if not self.pc_fold and not self.player_fold:
                    random_card = self.draw_card()
                    self.pc_deck.append(random_card)
                    self.player_move()

                elif not self.pc_fold and self.player_fold:
                    random_card = self.draw_card()
                    self.pc_deck.append(random_card)
                    self.pc_move()

                elif self.pc_fold and not self.player_fold:
                    self.player_move()

                elif self.pc_fold and self.player_fold:
                    self.decide_winner()

        elif self.pc_fold:
            self.player_move()


    def decide_winner(self):

        # print some info
        print('_' * 80)
        print("PC's CARDS:", self.pc_deck, '| ? -->', self.pc_deck[0])
        print("SUM OF PC'S CARDS:", sum(self.pc_deck))
        print('------------------------------------------')
        print("YOUR CARDS:", self.players_deck)
        print('SUM OF YOUR CARDS:', sum(self.players_deck))
        print('_' * 80)



        if sum(self.pc_deck) == 21 and sum(self.players_deck) != 21:
            print('')
            print('!!! PC HAS WON, YOU HAVE LOST !!!')


        elif sum(self.players_deck) == 21 and sum(self.pc_deck) != 21:
            print('')
            print('!!! YOU HAVE WON !!!')


        elif sum(self.players_deck) == 21 and sum(self.pc_deck) == 21:
            print('')
            print("!!! IT'S A DRAW !!!")


        elif sum(self.pc_deck) > 21 > sum(self.players_deck):
            print('')
            print('!!! YOU HAVE WON !!!')


        elif sum(self.players_deck) > 21 > sum(self.pc_deck):
            print('')
            print('!!! PC HAS WON, YOU HAVE LOST !!!')


        elif sum(self.players_deck) > 21 < sum(self.pc_deck):

            if sum(self.players_deck) < sum(self.pc_deck):
                print('')
                print('!!! YOU HAVE WON !!!')

            elif sum(self.pc_deck) < sum(self.players_deck):
                print('')
                print('!!! PC HAS WON, YOU HAVE LOST !!!')


            elif sum(self.players_deck) == sum(self.pc_deck):
                print('')
                print("!!! IT'S A DRAW !!!")


        elif sum(self.players_deck) < 21 > sum(self.pc_deck):

            if sum(self.players_deck) > sum(self.pc_deck):
                print('')
                print('!!! YOU HAVE WON !!!')

            elif sum(self.pc_deck) > sum(self.players_deck):
                print('')
                print('!!! PC HAS WON, YOU HAVE LOST !!!')

            elif sum(self.players_deck) == sum(self.pc_deck):
                print('')
                print("!!! IT'S A DRAW !!!")


a = RE_21()
