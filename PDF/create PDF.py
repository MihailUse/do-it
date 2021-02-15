#!/usr/bin/env python
# coding: utf-8

# In[24]:


from fpdf import FPDF


# In[52]:


pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True) #  шрифт для русского языка
pdf.set_font("DejaVu", size=12)

pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
pdf.ln(15) # переместить на 15 вниз 
pdf.cell(200, 10, txt="аывафпыырк авпвап hdfdfhgse to Python!", ln=1, align="R")
pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="L")

pdf.output("simple_demo.pdf")


# In[ ]:




