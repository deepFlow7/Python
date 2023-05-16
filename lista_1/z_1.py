import decimal as d

def vat_faktura(lista) :
    faktura = 0
    for x in lista :
        faktura += x
    faktura *= 1.23
    return round(faktura, 2)

def vat_paragon(lista) :
    paragon = 0
    for x in lista :
        brutto = 1.23 * x
        brutto = round(brutto, 2)
        paragon += brutto
    return paragon

zakupy = [0.2, 0.5, 4.59, 6]
print(vat_faktura(zakupy) == vat_paragon(zakupy)) # True

# z klasą Decimal

def vat_faktura_decimal(lista) :
    faktura = d.Decimal('0')
    for x in lista :
        faktura += x
    faktura *= d.Decimal('1.23')
    return round(faktura, 2)

def vat_paragon_decimal(lista) :
    paragon = d.Decimal('0')
    for x in lista :
        brutto = d.Decimal('1.23') * x
        brutto = round(brutto, 2)
        paragon += brutto
    return paragon

zakupy2 = [d.Decimal('0.2'), d.Decimal('0.5'), d.Decimal('4.59'), d.Decimal('6')]
print(vat_faktura_decimal(zakupy2) == vat_paragon_decimal(zakupy2)) # False



        