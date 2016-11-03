# SupremeAutoPurchase v1.0
#### SupremeAutoPurchase is a bot that will purchase new clothing drops on supremenewyork.com

###Requirements
- python 2.7
- firefox driver

####Installation
```sh install.sh```

####Usage
Modify config.ini with the product you wish to purchase, shipping information and payment info.
<br>
```Python buy.py```

Be specific about what product you wish to purchase.
The 'SelectOption' refers to the extra option for some products, in most cases it is a size parameter, occasionally it's a quantity field. If there is no size or quantity field then delete line 79 ``` browser.find_option_by_text(selectOption).first.click()```
I will make this automatic soon.


Thanks to @Hezion and @kaaetech for their help. They both have good forks of this project.


####11/3/16 Update
Finally pushing a new build. Good luck to everyone going for todays drop!
