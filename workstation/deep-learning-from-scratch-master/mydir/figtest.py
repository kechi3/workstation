import plotly.express as px
from skimage import io
img = io.imread('../dataset/lena.png')
fig = px.imshow(img)
fig.show()

