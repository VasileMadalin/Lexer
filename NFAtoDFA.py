import sys
from queue import Queue
# clasa care reprezinta un NFA
class NFA:
	# alphabet este o lista de caractere
	# delta un dictionar care primeste o pereche si returneaza un caracter
	# state0 starea initial
	# k lista de stari
	# statef lista cu starile finale
	def __init__(self, k, state0, statef, alph, function):
		self.k = k
		self.state0 = state0
		self.statef = statef
		self.alph = alph
		self.function = function

# clasa care reprezinta un DFA
class DFA:
	#alphabet este o lista de caractere
	#delta un dictionar care primeste o pereche si returneaza un caracter
	#state0 starea initial
	#k set de stari
	#statef lista cu starile finale
	def __init__(self, k, state0, statef, alph, delta):
		self.k = k
		self.state0 = state0
		self.statef = statef
		self.alph = alph
		self.delta = delta
		self.token = ""
		self.sinkstate = []
		for elem in self.k:
			ok = 1
			for func in self.delta:
				if elem == func[0]:
					if self.delta[func] != elem:
						ok = 0
			if ok == 1:
				self.sinkstate.append(elem)
 
# clasa care defineste o expresie regulata
class RegularExpression:
	# the class constructor.
	def __init__(self, string):
		self.string = string
	
	def __str__(self):
	  output = self.string
	  return output
 
# clasa STAR care mosteneste RegularExpression 
# si constrieste expresia folosind Prenex form
# se construieste o clasa pentru fiecare epresie regulata
# la fiecare expresie am adaugat campul nfa(fiind nfa-corespunzator expresiei)
class STAR(RegularExpression):
	def __init__(self, reg, type, nfa):
		self.reg = reg
		self.type = "STAR"
		self.nfa = nfa
	def __str__(self):
		output = ((self.reg).__str__()) + "*"
		return output

class PLUS(RegularExpression):
	def __init__(self, reg, type, nfa):
		self.reg = reg
		self.type = "PLUS"
		self.nfa = nfa
	def __str__(self):
		output = ((self.reg).__str__()) + "+"
		return output

class CONCAT(RegularExpression):
	def __init__(self, reg1, reg2, type, nfa):
		self.reg1 = reg1
		self.reg2 = reg2
		self.type = "CONCAT"
		self.nfa = nfa

	def __str__(self):
		output = "(" + ((self.reg1).__str__()) + ((self.reg2).__str__()) + ")"
		return output

class UNION(RegularExpression):
	def __init__(self, reg1, reg2, type, nfa):		
		self.reg1 = reg1
		self.reg2 = reg2
		self.type = "UNION"
		self.nfa = nfa

	def __str__(self):
		output = "(" + ((self.reg1).__str__()) + "U" + ((self.reg2).__str__()) + ")"
		return output

# metoda care verifica daca o expresie este rezultatul 
# unor expresii simple sau nu
def is_compound_form(e):
	if isinstance(e, UNION):
		return True
	if isinstance(e, CONCAT):
		return True
	if isinstance(e, STAR):
		return True
	if isinstance(e, PLUS):
		return True
	return False

# aceasta metoda modifca denumirea starilor unui NFA
# plecand de la o stare data ca paametru, 
# celelalte stari vor fi starea data din care se scade mereu 1
def transforme_neg(nfa1, new_state):
	new_k1 = []
	new_d1 = {}

	d1_help = {}
	for i in range(0, len(nfa1.k)):
		d1_help[nfa1.k[i]] = new_state
		new_k1.append(new_state)
		new_state = new_state - 1
	for elem in nfa1.function:
		p = elem[0]
		pprim = d1_help[p]
		listprim = []
		for stari in nfa1.function[elem]:
			listprim.append(d1_help[stari])

		new_d1[(pprim, elem[1])] = listprim
	new_state01 = d1_help[nfa1.state0]
	new_statef1 = d1_help[nfa1.statef]
	new_alph1 = nfa1.alph

	nfa1_aux = NFA(new_k1, new_state01, new_statef1, new_alph1, new_d1)
	return nfa1_aux

# aceasta metoda modifca denumirea starilor unui NFA
# plecand de la o stare data ca paametru, 
# celelalte stari vor fi starea data din care se aduna mereu 1
def transforme_pos(nfa1, new_state):
	new_k1 = []
	new_d1 = {}

	d1_help = {}
	for i in range(0, len(nfa1.k)):
		d1_help[nfa1.k[i]] = new_state
		new_k1.append(new_state)
		new_state = new_state + 1
	for elem in nfa1.function:
		p = elem[0]
		pprim = d1_help[p]
		listprim = []
		for stari in nfa1.function[elem]:
			listprim.append(d1_help[stari])

		new_d1[(pprim, elem[1])] = listprim
	new_state01 = d1_help[nfa1.state0]
	new_statef1 = d1_help[nfa1.statef]
	new_alph1 = nfa1.alph

	nfa1_aux = NFA(new_k1, new_state01, new_statef1, new_alph1, new_d1)
	return nfa1_aux

# metoda care elimina aparitiile suplimentare ale unor elemente dintr-o lista
# metoda folosita in algoritmul de convertire a unui NFA in DFA
def clean(listt):
	new_list = []
	for elem in listt:
		if elem not in new_list:
			new_list.append(elem)
	return new_list

# metoda care returneaza un NFA care este rezultatul concatenarii a doua NFA-uri
def concat(nfa1, nfa2):
	nr_stari_nfa1 = len(nfa1.k)
	# se modifica starile automatului(initial, ambele automate a stari 
	# pornind de la -1 in jos, apoi ambele de la 0 in sus)
	nfa1 = transforme_neg(nfa1, -1)
	nfa2 = transforme_neg(nfa2, -nr_stari_nfa1)
	nfa1 = transforme_pos(nfa1, 0)
	nfa2 = transforme_pos(nfa2, nr_stari_nfa1)
	aux_k = []
	aux_alph = []
	for elem in nfa1.alph:
		aux_alph.append(elem)
	for elem in nfa2.alph:
		aux_alph.append(elem)
	for elem in nfa1.k:
		aux_k.append(elem)
	for elem in nfa2.k:
		aux_k.append(elem)
	aux_d = {}
	for elem in nfa1.function:
		aux_d[elem] = nfa1.function[elem]
	for elem in nfa2.function:
		aux_d[elem] = nfa2.function[elem]
	aux_state0 = nfa1.state0
	aux_statef = nfa2.statef
	aux_d[(nfa1.statef, '&')] = []
	aux_d[(nfa1.statef, '&')].append(nfa2.state0)

	aux_alph = (clean(aux_alph))
	aux = NFA(aux_k, aux_state0, aux_statef, aux_alph, aux_d)
	return aux

# metoda care returneaza un NFA care este rezultatul reuniunii a doua NFA-uri
def union(nfa1, nfa2):
	# se modifica starile automatului(initial, ambele automate a stari 
	# pornind de la -1 in jos, apoi ambele de la 0 in sus)
	nr_stari_nfa1 = len(nfa1.k)
	nr_stari_nfa2 = len(nfa2.k)
	nfa1 = transforme_neg(nfa1, -1)
	nfa2 = transforme_neg(nfa2, -nr_stari_nfa1)
	nfa1 = transforme_pos(nfa1, 0)
	nfa2 = transforme_pos(nfa2, nr_stari_nfa1)
	index = nr_stari_nfa1 + nr_stari_nfa2
	aux_state0 = index
	aux_statef = index + 1
	
	aux_k = []
	aux_k.append(aux_state0)
	aux_k.append(aux_statef)
	aux_alph = []
	for elem in nfa1.alph:
		aux_alph.append(elem)
	for elem in nfa2.alph:
		aux_alph.append(elem)

	for elem in nfa1.k:
		aux_k.append(elem)
	for elem in nfa2.k:
		aux_k.append(elem)

	aux_d = {}
	for elem in nfa1.function:
		aux_d[elem] = nfa1.function[elem]
	for elem in nfa2.function:
		aux_d[elem] = nfa2.function[elem]
	aux_d[(aux_state0, '&')] = []
	aux_d[(aux_state0, '&')].append(nfa1.state0)	
	aux_d[(aux_state0, '&')].append(nfa2.state0)
	aux_d[(nfa1.statef, '&')] = []
	aux_d[(nfa1.statef, '&')].append(aux_statef)
	aux_d[(nfa2.statef, '&')] = []
	aux_d[(nfa2.statef, '&')].append(aux_statef)

	aux_alph = (clean(aux_alph))	
	aux = NFA(aux_k, aux_state0, aux_statef, aux_alph, aux_d)
	return aux	

# metoda care returneaza un NFA care este rezultatul aplicarii star peste un automat
def star(nfa1):
	nr_stari_nfa1 = len(nfa1.k)
	# starile mai intai devine negative, apoi pozitive, 
	# pentru a fi siguri ca sunt numeroate de la 0
	nfa1 = transforme_neg(nfa1, -1)
	nfa1 = transforme_pos(nfa1, 0)
	index = nr_stari_nfa1
	aux_state0 = index
	aux_statef = index + 1
	aux_k = []
	aux_k.append(aux_state0)
	aux_k.append(aux_statef)
	aux_alph = []
	for elem in nfa1.alph:
		aux_alph.append(elem)
	for elem in nfa1.k:
		aux_k.append(elem)
	aux_d = {}
	for elem in nfa1.function:
		aux_d[elem] = nfa1.function[elem]
	aux_d[(aux_state0, '&')] = []
	aux_d[(aux_state0, '&')].append(nfa1.state0)

	aux_d[(nfa1.statef, '&')] = []
	aux_d[(nfa1.statef, '&')].append(aux_statef)
	aux_d[(aux_state0, '&')].append(aux_statef)

	aux_d[(nfa1.statef, '&')].append(nfa1.state0)

	aux_alph = (clean(aux_alph))
	aux = NFA(aux_k, aux_state0, aux_statef, aux_alph, aux_d)
	return aux

# metoda care returneaza un NFA care este rezultatul aplicarii star peste un automat
def plus(nfa1):
	nr_stari_nfa1 = len(nfa1.k)
	# starile mai intai devine negative, apoi pozitive, 
	# pentru a fi siguri ca sunt numeroate de la 0
	nfa1 = transforme_neg(nfa1, -1)
	nfa1 = transforme_pos(nfa1, 0)
	index = nr_stari_nfa1
	aux_state0 = index
	aux_statef = index + 1
	aux_k = []
	aux_k.append(aux_state0)
	aux_k.append(aux_statef)
	aux_alph = []
	for elem in nfa1.alph:
		aux_alph.append(elem)
	for elem in nfa1.k:
		aux_k.append(elem)
	aux_d = {}
	for elem in nfa1.function:
		aux_d[elem] = nfa1.function[elem]
	aux_d[(aux_state0, '&')] = []
	aux_d[(aux_state0, '&')].append(nfa1.state0)

	aux_d[(nfa1.statef, '&')] = []
	aux_d[(nfa1.statef, '&')].append(aux_statef)
	#aux_d[(aux_state0, '&')].append(aux_statef)

	aux_d[(nfa1.statef, '&')].append(nfa1.state0)

	aux_alph = (clean(aux_alph))
	aux = NFA(aux_k, aux_state0, aux_statef, aux_alph, aux_d)
	return aux;
# metoda care returneaza un NFA care este rezultatul unei 
# expresii regulate simple
def character(ch):
	aux_state0 = 0
	aux_statef = 1
	aux_k = [0, 1]
	aux_alph = []
	aux_alph.append(ch)
	aux_d = {}
	aux_d[(aux_state0, ch)] = []
	aux_d[(aux_state0, ch)].append(aux_statef)
	aux = NFA(aux_k, aux_state0, aux_statef, aux_alph, aux_d)
	return aux

# metoda folosita pentru gasirea starilor care sunt legate prin 
# epsilon transition de alte stari, astfel reducand numarul de stari
# metoda folosita in algoritmul de convertirea a unui NFA in DFA
def FindEpsilonTransition(nfa, stare):
	pair = (stare, '&')
	if pair in nfa.function:
		return nfa.function[pair]
	return False

# metoda care ne indica daca o stare nou creata este finala sau nu(daca include
# stare finala din automatul intial)
# metoda folosita in algoritmul de convertire a unui NFA in DFA
def CheckFinalState(lista, stare_finala_nfa):
	for elem in lista:
		if elem == stare_finala_nfa:
			return True
	return False

# metoda care gaseste starile care sunt legate prin epsilon transtion de alte 
# stari(verifica pentru fiecare stare din starea compuse primita ca parametru) 
# si la final le adauga in stare compuse primita ca parametru 
# metoda folosita in algoritmul de convertire a unui NFA in DFA
def FindStatesConnectedByEpsilon(current_states, nfa):
	aux_current_states = []
	for current_state in current_states:
		pair = (current_state, '&')
		if pair in nfa.function:
			initial_epsilon = nfa.function[pair]
			for elem in initial_epsilon:
				if elem not in current_states:
					aux_current_states.append(elem)
	aux_current_states = aux_current_states+current_states
	aux_current_states = clean(aux_current_states)
	aux_current_states.sort()
	return aux_current_states

# metoda care aplica algoritmul de conversie de la NFA la DFA
def convertNFAtoDFA(nfa):
	# prima stare compusa este formata din starea initala a autoamtului
	start_current_states = [nfa.state0]
	queue = Queue()
	# se adauga starea curenta pe o coada, pentru a fi procesata
	queue.put(start_current_states)
	
	# se intializeaza campurile DFA-ului cu stari compuse
	dfa_states = []
	dfa_delta = {}
	final_states = []

	# cat timp avem stari de procesat in coada, se ruleaza algoritmul
	while queue.empty() is not True:
		OK = True
		current_states = queue.get()
		dfa_states.append(current_states)
		# daca stare curenta compusa contine stari care sunt finale, 
		# atunci aceasta se adauga la lista cu stari finale ale noului automat 
		if CheckFinalState(current_states, nfa.statef):
				final_states.append(current_states)

		initial_epsilon = []
		aux_current_states = []

		# se cauta in starea curenta, daca vreo stare din aceasta este legata 
		# prin epsilon transition de alta stari daca da, se adauga la starea 
		# curenta si se reia algoritmul cu starea nou formata
		for current_state in current_states:
			pair = (current_state, '&')
			if pair in nfa.function:
				initial_epsilon = nfa.function[pair]
				for elem in initial_epsilon:
					if elem not in current_states:
						aux_current_states.append(elem)
						OK = False
		# nu sunt epsilon tranzitii
		if OK == True:
			# se adauga starea la lista cu stari alea automatului
			dfa_states.append(current_states)
			d = {}
			# se aplica algoritmul propriu-zis(din fiecare stare se verifica 
			# fiecare caracter in ce stari poate duce)
			# folosim un dictionar pentru  a tine cont de starile in care se 
			# poate ajunge dace se pleca de la o stare cu un anumit caracter
			# se tine cont si de epsilon tranzition atunci cand se gaseste o stare noua
			for current_state in current_states:
				for ch in nfa.alph:
					pair = (current_state, ch)
					final_lista_stari = []
					if pair in nfa.function:
						lista_stari = nfa.function[pair]
						aux_list_stari_epsilon = []
						for stare in lista_stari:
							epsilon_list = FindEpsilonTransition(nfa, stare)
							if epsilon_list is not False:
								aux_list_stari_epsilon = epsilon_list
						final_lista_stari = lista_stari+aux_list_stari_epsilon
						final_lista_stari = clean(final_lista_stari)
					if ch not in d:
						d[ch] = final_lista_stari
					else:
						d[ch] = d[ch]+final_lista_stari
			ok = True
			aux_list = []
			# se parcurge dictionarul care ne zice in ce stari ne duce fiecare caracter
			for elem in d:
				list = clean(d[elem])
				list.sort()
				if list:
					if list not in aux_list and list not in dfa_states:
						aux_list.append(list)
					# pentru fiecare stare compusa, cautam si epsilon tranzitiile
					states_connected_by_epsilon = FindStatesConnectedByEpsilon(list, nfa)
					states_connected_by_epsilon_aux = FindStatesConnectedByEpsilon(states_connected_by_epsilon, nfa)
					# dupa ce am adugat si epsilon tranziile ale tuturor starilor 
					# care pot generea alte epsilon tranzitii
					while states_connected_by_epsilon_aux != states_connected_by_epsilon:
						states_connected_by_epsilon = states_connected_by_epsilon_aux
						states_connected_by_epsilon_aux = FindStatesConnectedByEpsilon(states_connected_by_epsilon, nfa)
					# se creeaza noua configuratie din functia delta
					dfa_delta[(str(current_states), elem)] = str(states_connected_by_epsilon_aux)
					# daca starile sunt finale, se adauga in lista cu stari finale
					if CheckFinalState(states_connected_by_epsilon, nfa.statef):
						final_states.append(states_connected_by_epsilon)
			# daca am gasit stari in care putem ajunge, si nu au fost deja exploatate, 
			# se adauga in coada pentru a fi procesate
			if aux_list: 
				for elem in aux_list:
					if elem not in dfa_states:
						queue.put(elem)
		# daca se gasesc epsilon tranzitii, acestea se adauga la starea curenta 
		# si se modifica toate aparitiile acestei stari
		else:
			aux_current_states = aux_current_states+current_states
			aux_current_states = clean(aux_current_states)
			aux_current_states.sort()
			for elem in dfa_delta:
				if dfa_delta[elem] == str(current_states):
					dfa_delta[elem] = str(aux_current_states)
			queue.put(aux_current_states)
	######################################################################################
	# in acest moment DFA -ul are stari compuse, urmeaza sa 
	# transformam aceste stari in stari simple, numerotate de la 0
	new_states = []	# lista cu noile stari
	new_final_states = [] # lista cu noile stari finale
	new_states_coresp = {} # un dictionar care face corespondenta intre starile vechi si cele noi
	index = 0
	# se realizeaza corespondenta intre starile vechi(cele compuse) in cele noi(indexate de la 0)
	for elem in dfa_delta:
		if elem[0] not in new_states_coresp:
			new_states_coresp[elem[0]] = index
			new_states.append(index)
			index = index + 1
		if dfa_delta[elem] not in new_states_coresp:
			new_states_coresp[dfa_delta[elem]] = index
			new_states.append(index)
			index = index + 1

	# se creeaza noul dictionar(functie a dfa-ul)
	new_dfa_delta = {}
	for elem in dfa_delta:
		key = (new_states_coresp[elem[0]], elem[1])
		value = new_states_coresp[dfa_delta[elem]]
		new_dfa_delta[key] = value

	# se creeaza lista cu stari finale
	for elem in final_states:
		stari_compuse = str(elem)
		if stari_compuse in new_states_coresp:
			if new_states_coresp[stari_compuse] not in new_final_states:
				# se adauga in lista starea care corespunde fiecarei stari 
				# finale din automatul cu stari compuse
				new_final_states.append(new_states_coresp[stari_compuse])
	
	# stare intiala este prima care a fost adugata in pricesul 
	# de transformare NFA in dfa
	new_state_initial = -1
	for elem in new_states_coresp:
		new_state_initial = new_states_coresp[elem]
		break

	# se sorteaza alfabetul
	nfa.alph.sort()
	# facem functia dictionarului sa fie completa, adaugand un sink state
	new_states.append(index)
	for i in range(0, index + 1):
		for ch in nfa.alph:
			pair = (i, ch)
			if pair not in new_dfa_delta:
				new_dfa_delta[pair] = index
	# se creeaza obiectul propriu zis al automatului final si se returneaza
	dfa = DFA(new_states, new_state_initial, new_final_states, nfa.alph, new_dfa_delta)
	return dfa

