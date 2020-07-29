# -*- coding: utf-8 -*-

from MyQR import myqr
from tqdm import tqdm
import time

# myqr.run(
#     words='https://m.v.qq.com/play.html?vid=i0733wqy4hw&ptag=v_qq_com%23v.play.adaptor%233&second_share=1&from=timeline',
#     picture='22.jpg',
#     colorized=True,
#     save_name='ok.png'
# )

for i in tqdm(range(100000)):
    # print(i, end='|')
    time.sleep(0.05)

