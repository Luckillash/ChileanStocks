import yfinance as yf
import pandas as pd
import os

# Configura los símbolos de las acciones que deseas obtener de la Bolsa de Santiago
symbols = [
    'AAISA.SN', 'AFPCAPITAL.SN', 'AGUAS-A.SN', 'ALMENDRAL.SN', 'ANTARCHILE.SN',
    'AZUL-AZUL.SN', 'BANVIDA.SN', 'BCI.SN', 'BESALCO.SN', 'BETLAN-DOS.SN',
    'BICECORP.SN', 'BINT.SN', 'BLUMAR.SN', 'BOLSASTGO.SN', 'BSANTANDER.SN',
    'CALICHERAA.SN', 'CAMANCHACA.SN', 'CAMPOS.SN', 'CAP.SN', 'CAROZZI.SN',
    'CCU.SN', 'CEMENTOS.SN', 'CENCOMALLS.SN', 'CENCOSUD.SN', 'CGE.SN',
    'CGET.SN', 'CHILE.SN', 'CIC.SN', 'CINTAC.SN', 'CMPC.SN', 'COLBUN.SN',
    'COLO-COLO.SN', 'CONCHATORO.SN', 'CONSOGRAL.SN', 'COPEC.SN', 'CRISTALES.SN',
    'CRUZADOS.SN', 'CTC.SN', 'CUPRUM.SN', 'DUNCANFOX.SN', 'ECL.SN',
    'EDELMAG.SN', 'EISA.SN', 'ELECMETAL.SN', 'ENAEX.SN', 'ENELAM.SN',
    'ENELCHILE.SN', 'ENELDXCH.SN', 'ENELGXCH.SN', 'ENJOY.SN', 'ENLASA.SN',
    'ENTEL.SN', 'ESVAL-C.SN', 'FALABELLA.SN', 'FORUS.SN', 'FOSFOROS.SN',
    'GASCO.SN', 'HABITAT.SN', 'HIPERMARC.SN', 'HITES.SN', 'IAM.SN',
    'IANSA.SN', 'ILC.SN', 'INDISA.SN', 'INGEVEC.SN', 'INVERCAP.SN',
    'INVERNOVA.SN', 'ISANPA.SN', 'ITAUCL.SN', 'LAS-CONDES.SN', 'LIPIGAS.SN',
    'LTM.SN', 'MALLPLAZA.SN', 'MANQUEHUE.SN', 'MARINSA.SN', 'MASISA.SN',
    'MELON.SN', 'MINERA.SN', 'MOLLER.SN', 'MULTI-X.SN', 'NAVIERA.SN',
    'NITRATOS.SN', 'NORTEGRAN.SN', 'NTGCLGAS.SN', 'NUAM.SN', 'NUEVAPOLAR.SN',
    'NUTRAVALOR.SN', 'ORO-BLANCO.SN', 'OXIQUIM.SN', 'PARAUCO.SN', 'PASUR.SN',
    'PAZ.SN', 'PEHUENCHE.SN', 'PLANVITAL.SN', 'POLO.SN', 'POTASIOS-A.SN',
    'PREVISION.SN', 'PROVIDA.SN', 'PUCOBRE.SN', 'QUILICURA.SN', 'QUINENCO.SN',
    'RIPLEY.SN', 'SALFACORP.SN', 'SALMOCAM.SN', 'SCHWAGER.SN', 'SCOTIABKCL.SN',
    'SECURITY.SN', 'SIEMEL.SN', 'SK.SN', 'SMSAAM.SN', 'SMU.SM', 'SOCOVESA.SN',
    'SONDA.SN', 'SOQUICOM.SN', 'SPORTING.SN', 'SQM-A.SN', 'TRICAHUE.SN',
    'TRICOT.SN', 'VAPORES.SN', 'VENTANAS.SN', 'VOLCAN.SN', 'VSPT.SN',
    'WATTS.SN', 'ZOFRI.SN'
]  # Ejemplo de acciones de la bolsa de Santiago

# Archivo donde se almacenarán los datos
output_file = 'acciones_chilenas.txt'

# Función para escribir los datos en el archivo
def write_data_to_file(data_dict):
    existing_data = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_data = f.readlines()
    with open(output_file, 'w') as f:
        for date, entries in sorted(data_dict.items(), reverse=True):
            for entry in entries:
                f.write(entry + '\n')
        for line in existing_data:
            f.write(line)

    print("Proceso finalizado correctamente.")


# Función para obtener la última fecha registrada en el archivo
def get_last_date():
    if not os.path.exists(output_file):
        return None
    with open(output_file, 'r') as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1]
            last_date = last_line.split(',')[1]
            return pd.to_datetime(last_date).date()
    return None

# Obtener la última fecha registrada
last_date = get_last_date()

# Descargar datos históricos de las acciones
data_dict = {}
for symbol in symbols:
    
    print(symbol)

    stock = yf.Ticker(symbol)
    
    if last_date:
        # Si el archivo ya existe, descarga datos desde la última fecha registrada
        data = stock.history(start=last_date + pd.DateOffset(days=1))
    else:
        # Si el archivo no existe, descarga todos los datos históricos
        data = stock.history(period="max")

    # Organizar los datos por fecha
    for index, row in data.iterrows():
        date_str = index.strftime('%Y%m%d')
        if date_str not in data_dict:
            data_dict[date_str] = []
        entry = f"{symbol},{date_str},{row['Open']},{row['High']},{row['Low']},{row['Close']},{row['Volume']}"
        data_dict[date_str].append(entry)

# Escribir los datos en el archivo
write_data_to_file(data_dict)

