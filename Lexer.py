import NFAtoDFA

# metoda care genereaza starea urmatoare pentru un automat aflat
# intr-o stare si primeste un caracter nou
def execute(letter, dfa, state):
   p = (state, letter)
   if p in dfa.delta:
      return dfa.delta[p]
   return False

# metoda care verifica daca un automat a inceput sa respinga inputul 
# unui cuvant
def ready_automata(ok):
   if ok == -1:
      return True   
   return False

# metoda care ruleaza lexer-ul propriu-zis
def runlexer(DFAs1, sequence_file, output_file):
   DFAs = DFAs1

   # se deschide fisierul care contine secventa de procesat
   file_sequence = open(sequence_file, 'r')
   sequence = file_sequence.read()
   
   # folosind i ca sa parcurgem cuvantul
   i = 0

   # o lista care contine starile initiale ale automatelor
   stateCurrent = []
   # o lista are contine etapa in care se afla automatele(acceptare, neaceptare, sinkstate)
   okDFA = []

   # lista care contine cuvintele acceptate de fiecare automat urmand sa fie ales cel mai lung
   lexems = []
   # lista care contine starile urmatoare ale automatelor
   next_state = []

   #initializare variabile locale
   for j in range(0, len(DFAs)):
      stateCurrent.append(DFAs[j].state0)
      okDFA.append(0)
      lexems.append("")
      next_state.append("")

   # lugimea maxima a cuvantul gasit
   maximum_length = -1
   # ind_dfaicile pe automatului care a gasit cuvantul
   ind_dfa = -1
   # string-ul in care se memoreaza lexem-ul curent
   current_lexem = ""
   # string-ul in care se memeoreaza lexem-ul acceptat de un automat
   accepted_lexem = ""
   # variabile care ne zice daca cel putin unul din automate a acceptat un cuvant
   OK = 0
   # strng-ul in care se scrie output-ul
   output = ""
   # pozitia in care s-a acceptat un cuvant
   last_i = -1
   # variabila care ind_dfaica o eroare
   lexer_error = -1
   # varibila care ind_dfaica pozitia ultimului caracter care a fost acceptat
   # (folosita in caz de eroare)
   last_correct_input = -1
   #variabila care indica numarul de linii noi, in cazul afisarii unei erori
   new_lines_number = 0
   while i < len(sequence):
      if sequence[i] == '\n':
         new_lines_number = new_lines_number + 1
      # se adauga fiecare caracter in lexemul corent care urmeaza sa fie procesat
      current_lexem = current_lexem + sequence[i]
      # se gaseste stare urmatoare pentru fiecare automat
      for j in range(0, len(DFAs)):
         if okDFA[j] != -1:
            next_state[j] = execute(sequence[i], DFAs[j], stateCurrent[j])
            #print(str(next_state[j]) + "*" + DFAs[j].token)
            if next_state[j] == False:
               okDFA[j] = -1
            else:
               if next_state[j] in DFAs[j].sinkstate:
                  okDFA[j] = -1
               else:
                  last_correct_input = i
         else:
            next_state[j] = False
      # daca automatul ajunge in stare finala, cuvantul este acceptat
      for j in range(0, len(DFAs)):
         if next_state[j] in DFAs[j].statef and next_state[j] != DFAs[j].state0:
            #print("$" + DFAs[j].token)
            lexems[j] = current_lexem
            okDFA[j] = 1
      # se gaseste cel mai mare mare lexem acceptat de unul dintre automate
      for j in range(0, len(DFAs)):
         if okDFA[j] == 1:
            OK = 1
            if len(lexems[j]) > maximum_length:
               final_lexem = lexems[j]
               last_i = i
               maximum_length = len(lexems[j])
               ind_dfa = j
      # daca se ajunge la finalul secventei, "se opresc" toate automatele 
      if i + 1 == len(sequence): 
         for j in range(0, len(DFAs)):
            okDFA[j] = -1
      # se verifica daca toate automatele au respins caracterul curent
      situation = True
      for j in range(0, len(DFAs)):
         situation = situation and ready_automata(okDFA[j])
      # daca toate automatele au respins caracterul curent si cel putin unul a acceptat anterior
      if situation and OK == 1:
         string = ""
         #print("*****")
         for k in range(0, len(final_lexem)):
            if final_lexem[k] == '\n':
               string = string + "\\n"
            else:
               string = string + final_lexem[k]
         # se adauga in output lexem-ul gasit
         output = output + DFAs[ind_dfa].token + " " + string + "\n"
         # se reinitializeaza automatele
         for j in range(0, len(DFAs)):
            stateCurrent[j] = DFAs[j].state0
            okDFA[j] = 0
            lexems[j] = ""
         i = last_i + 1
         maximum_length = -1
         ind_dfa = -1
         last_i = -1
         OK  = 0
         current_lexem = ""
      # daca nu se accepta un cuvant inca, se trece la urmatorul caracter
      else:
         # daca nu se accepta niciun cuvant, se afiseaza o eroare
         if i == len(sequence) - 1:
            lexer_error = last_correct_input
         for j in range(0, len(DFAs)):
            stateCurrent[j] = next_state[j]
         i = i + 1
   f = open(output_file, "w+")
   # se afiseaza token-urile + lexemele, daca avem eroare, se afiseaza un mesaj corespunzator 
   if lexer_error != -1:
      aux_string = ""
      if lexer_error + 1 == len(sequence):
         aux_string = "EOF"
      else:
         aux_string = str(lexer_error + 1)

      output = "No viable alternative at character "+ aux_string + ", line " + str(new_lines_number)
      f.write(output)
   else:
      if output == "":
         output = "No viable alternative at character 0 , line "+ str(new_lines_number) + "\n"
      f.write(output[:-1])



