import pickle

def pick(dic):
	dic_file = open('dic.pickle', 'ab')
	pickle.dump(dic, dic_file)
	dic_file.close()

def unpick():
	dic_file = open('dic.pickle', 'rb')
	dic = pickle.load(dic_file)
	dic_file.close()