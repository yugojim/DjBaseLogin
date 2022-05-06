import requests
import json
import math

fhir = 'http://192.168.1.119:8001/fhir/'
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
def post_dbSNP(fhir=fhir, Alleles='', dbSNP='',payload={}):
    Observationurl=fhir+'Observation?'
    Alleles = Alleles
    dbSNP = dbSNP
    try:
        #print(Alleles,dbSNP)
        #Alleles='T/A'
        #dbSNP='rs9939609'
        dbSNPObservationUrl = Observationurl+'value-string='+Alleles+'%20at%20SNP%20'+dbSNP+'&_elements=subject&_count=500'
        dbSNPObservationCountUrl = Observationurl+'value-string='+Alleles+'%20at%20SNP%20'+dbSNP+'&_summary=count'
        #print(getObservationurl,headers,payload)
        dbSNPCount = requests.request("GET", dbSNPObservationCountUrl, headers=headers, data=payload)
        #print(Observationresponse.text)
        dbSNPCountjson=json.loads(dbSNPCount.text)
        dbSNPresponse = requests.request("GET", dbSNPObservationUrl, headers=headers, data=payload)
        #print(Observationresponse.text)
        dbSNPresponsejson=json.loads(dbSNPresponse.text)
        count=dbSNPCountjson['total']
        data=dbSNPresponsejson['entry']
        link=dbSNPresponsejson['link']
        context = {
                'count' : count,
                'data' : data,
                'link' : link
                }
        return context
    except:
        return None
    
def post_data(fhir = fhir,PatientID='',payload={}):
    try:
        Observationurl=fhir+'Observation?'
        PatientID = PatientID
        getObservationurl = Observationurl+'subject='+PatientID.replace('_','-')
        #print(getObservationurl,headers,payload)
        Observationresponse = requests.request("GET", getObservationurl, headers=headers, data=payload)
        #print(Observationresponse.text)
        ObservationResultjson=json.loads(Observationresponse.text)
        HBBlist=[]
        Obes_list=[]
        ABCG2list=[]
        ALDH2list=[]
        NOTCH3list=[]
        LDLRlist=[]
        CYP2C19list=[]
        PCSK9list=[]
        APOBlist=[]
        KCNJ11list=[]
        ABCC8list=[] 
        HNF4Alist=[]
        HNF1Alist=[]
        GCKlist=[]
        TPMTlist=[]
        cycle=math.ceil(ObservationResultjson['total']/20)
        if cycle > 0:
            for page in range(1,cycle):
                 pageurl='&_getpagesoffset='+str(page*20)
                 #print(getObservationurl+pageurl)
                 pageurlresponse = requests.request("GET", getObservationurl+pageurl, headers=headers, data=payload)
                 pageurlResultjson=json.loads(pageurlresponse.text)
                 ObservationResultjson['entry'].extend(pageurlResultjson['entry'])
        #print(ObservationResultjson['total'])
        for i in range(ObservationResultjson['total']):
            #print(i)
            #print(ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code'])
            
            ##51968-6
            if ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code']=='51968-6':
               #print(ObservationResultjson['entry'][i]['resource']['component'][0]['valueString'])
                final_comment=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
            ##diagnostic-implication
            elif ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code']=='diagnostic-implication':
                #print(ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code'],i)
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='65959000':
                    #print(ObservationResultjson['entry'][i]['resource']['component'][0]['valueString'])
                    HBB_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                    #print(HBB_risk)
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='414916001':
                    Obes_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='398036000':
                    FH_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='609561005':
                    MODY_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='Azathioprine藥物代謝風險':
                    TPMT_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='clopidogrel藥物代謝風險':
                    CYP2C19_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                    #print(CYP2C19_risk)
            
            ##84413-4
            elif ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code']=='84413-4':
                #print(ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='HBB':
                    #print(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                    HBBlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                    #print(HBBlist)
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='FTO':
                    Obes_list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='ABCG2':
                    ABCG2list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                                        
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='ALDH2':
                    ALDH2list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='NOTCH3':
                    NOTCH3list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                                               
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='CYP2C19':
                    CYP2C19list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='LDLR':
                    LDLRlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='PCSK9':
                    PCSK9list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='APOB':
                    APOBlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='ABCC8':
                    ABCC8list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='KCNJ11':
                    KCNJ11list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='HNF4A':
                    HNF4Alist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='HNF1A':
                    HNF1Alist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                    
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='GCK':
                    GCKlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                    
                if ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display']=='TPMT':
                    TPMTlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                    
            else:
                None
            
        context = {
                'PatientID' : PatientID,
                'ALDH2list' : ALDH2list,
                'Obes_list' : Obes_list,
                'ABCG2list' : ABCG2list,
                'HBBlist' : HBBlist,
                'LDLRlist' : LDLRlist,
                'PCSK9list' : PCSK9list,
                'APOBlist' : APOBlist,
                'NOTCH3list' : NOTCH3list,
                'CYP2C19list' : CYP2C19list,
                'KCNJ11list' : KCNJ11list,
                'ABCC8list' : ABCC8list,
                'HNF4Alist' : HNF4Alist,
                'HNF1Alist' : HNF1Alist,
                'GCKlist' : GCKlist,
                'TPMTlist' : TPMTlist,
                'HBB_risk' : HBB_risk,
                'Obes_risk' : Obes_risk,
                'FH_risk' : FH_risk,
                'MODY_risk' : MODY_risk,
                'CYP2C19_risk' : CYP2C19_risk,
                'TPMT_risk' : TPMT_risk,
                'final_comment' : final_comment
                }
        #print(context)
        return context
    except:
        return None