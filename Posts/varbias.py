import numpy as np
import matplotlib.pyplot as plt

def plot_stats(data, reference=None, subplot=False):  
	x = np.arange(len(data))
	means = np.mean(data, axis=1)
	varss = np.var(data, axis=1)
	plt.plot(x, means, 'b-')
	plt.fill_between(x, means-varss, means+varss, facecolor='#96c9ff')
	if not subplot:
		plt.title('f(x) vs x')
		plt.xlabel('x')
		plt.ylabel('f(x)')

	if reference is not None:
		plt.plot(x, reference, 'g', linewidth=1)
	plt.legend(['f(x)', 'F(x)'])
	if not subplot:
		plt.show()

def get_data(samples, noise_scale, bias_scale=1):
	data = []
	for i in range(1, 40):
		curItems = []
		for j in range(samples):
			curItems.append(bias_scale*np.log(i) + noise_scale*np.random.uniform(-1, 1))
		data.append(curItems)

	ref = [np.log(i) for i in range(1, 40)]
	return data, ref

#data, ref = get_data(60, 1, 1.1)
#plot_stats(data, reference=ref)

# fig = plt.figure(figsize=(9, 9))
# p = 1

# for x in range(4):
# 	for y in range(4):
# 		ax = plt.subplot(4, 4, p)
# 		d, ref = get_data((x+1)*10, 2.5-0.5*y)
# 		plot_stats(d, ref, subplot=True)
# 		formatter = 'samples={}, noise={:.2f}'.format((x+1)*10, 2.5-0.5*y)
# 		ax.set_title(formatter, fontsize=8)
# 		p += 1


fig = plt.figure(figsize=(10, 3))

p = 1
for x in range(4):
	ax = plt.subplot(1, 4, p)
	bias_scale = 1+x*0.05

	d, ref = get_data(40, 1, bias_scale)
	plot_stats(d, ref, subplot=True)
	formatter = 'samples={}, bias_scale={:.2f}'.format(40, bias_scale)
	ax.set_title(formatter, fontsize=8)
	p += 1
	
plt.tight_layout()
plt.show()