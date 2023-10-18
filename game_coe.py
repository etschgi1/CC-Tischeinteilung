import numpy as np
from fpdf import FPDF
# COE Spiel CC 2023 Frühjahr
# TODO: Tischnummern ausdrucken für die Tische -> Spieler pro Tisch (zumindest anzahl wissen)
# Begriffe nie zwischen selben Tisch matchen!
number_people_on_table = [10, 10, 10, 10, 10, 10, 10,
                          10, 10, 10]  # number of persons on tables
TOTAL_PLAYERS = 90
Word_pairs = [('Fleiß', 'Belohnung'), ('Brot', 'Brötchen'), ('Hund', 'Katze'), ('Sonne', 'Mond'), ('Zahnbürste', 'Zahnseide'), ('Schwarz', 'Weiß'), ('Oben', 'Unten'), ('Feuer', 'Brand'), ('Kaffee', 'Tee'), ('Messer', 'Gabel'), ('Links', 'Rechts'), ('Tag', 'Nacht'), ('Wald', 'Baum'), ('Hose', 'Hemd'), ('Auge', 'Ohr'), ('Hand', 'Fuß'), ('Tisch', 'Stuhl'),
              ('Auto', 'Fahrrad'), ('Haus', 'Gebäude'), ('Huhn', 'Ei'), ('Apfel', 'Birne'), ('Rebe', 'Wein'), ('Licht', 'Dunkelheit'), ('Blume', 'Garten'), ('Himmel', 'Wolken'), ('Teich', 'See'), ('Frühling', 'Sommer'), ('Berg', 'Tal'), ('Schiff', 'Hafen'), ('Flügel', 'Vogel'), ('Gold', 'Silber'), ('Schlüssel', 'Schloss'), ('Hut', 'Mütze'), ('Maus', 'Tastatur'), ('Stern', 'Galaxie'), ('Liebe', 'Hass'), ('Wahrheit', 'Lüge'), ('Freiheit', 'Gefangenschaft'), ('Glück', 'Pech'), ('Lachen', 'Weinen'), ('Jung', 'Alt'), ('Nord', 'Süd'), ('Ost', 'West'), ('Geben', 'Nehmen'), ('Radio', 'Fernsehen'), ('Stadt', 'Land'), ('Tasche', 'Koffer'), ('Kamm', 'Bürste'), ('Telefon', 'Handy'), ('Kino', 'Film'), ('Mutter', 'Vater'), ('Sand', 'Strand'), ('Bus', 'Bahn'), ('Eis', 'Schnee'), ('Flugzeug', 'Hubschrauber'), ('Uhr', 'Wecker')]
print("Wortanzahl: " + str(len(Word_pairs) * 2))


def check_uniqueness(word_list):
    words_in_one_list = []
    for word_pair in word_list:
        words_in_one_list.append(word_pair[0])
        words_in_one_list.append(word_pair[1])
    for word in words_in_one_list:
        if words_in_one_list.count(word) > 1:
            print("Word " + word + " is not unique!")
            return False
    print("All words are unique!")
    return words_in_one_list


def assign_words_to_tables(word_list, people_on_table, checknum_len=5, maxit=1000):
    Id_to_word_pair = {}
    people_on_table_orig = people_on_table.copy()
    table_max_index = len(people_on_table) - 1
    c = 0
    for word1, word2 in word_list:
        print(c)
        c += 1
        it = maxit
        while True:
            it -= 1
            if it == 0:
                break
            # two random table_indices not same
            idx_1, idx_2 = np.random.choice(
                range(table_max_index + 1), 2, replace=False)
            if people_on_table[idx_1] == 0 or people_on_table[idx_2] == 0:
                continue
            rand_id = np.random.randint(10**checknum_len)
            if rand_id not in Id_to_word_pair.keys():
                Id_to_word_pair[rand_id] = (
                    (word1, idx_1 + 1), (word2, idx_2 + 1))
                people_on_table[idx_1] -= 1
                people_on_table[idx_2] -= 1
                break
    print("Remaining people on tables: " + str(people_on_table))
    if sum(people_on_table) != 0:
        print("Not all people are assigned to a table! - Try again")
        assign_words_to_tables(word_list, people_on_table_orig)
    return Id_to_word_pair


class PDF(FPDF):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Add a method to create the table
    def create_table(self, data, col_width=[25, 50, 10, 25, 50, 10], row_height=10):

        # Set font and cell padding
        self.set_font('Arial', '', 16)
        # self.cell(0, 10, '', 0, 1)
        # self.cell(col_width, row_height, '', border=1)
        self.set_fill_color(200, 200, 200)

        # Add column headers
        for i, column in enumerate(data[0]):
            self.cell(col_width[i], row_height, column, border=1, fill=True)

        # Add table data
        self.ln()
        self.set_fill_color(255, 255, 255)
        for row in (data[1:]):
            for i, item in enumerate(row):
                self.cell(col_width[i], row_height, str(
                    item), border=1, fill=True)
            self.ln()


def create_pdf(Id_to_word_pair):
    pdf = PDF()
    pdf.add_page()
    header = ["ID1", "Wort1", "T1", "ID2",
              "Wort2", "T2"]
    # create pdf table
    data = [header]
    for key, value in Id_to_word_pair.items():
        data.append([key, value[0][0], value[0][1],
                    key, value[1][0], value[1][1]])
    pdf.create_table(data)
    pdf.output("word_pairs.pdf", "F")


words = check_uniqueness(Word_pairs)
if words:
    res = (assign_words_to_tables(Word_pairs, number_people_on_table))
    print(f"Got {len(res)} word pairs")
    create_pdf(res)
