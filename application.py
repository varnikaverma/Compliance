from flask import Flask, request, render_template
import os
import glob
import fitz
import json
import urllib.request
import pickle
from calculate import get_ratio, count
from ami import ami_extract_details
from form import extract_details
from fid import fid_extract_details
from mer import mer_extract_details
from sch import sch_extract_details
from dl import dl_extract_details
from ss import ss_extract_details
from extra import extra_dets
from subcatschwab import subcat_schwab_extract_details
from checkbox import composed_model_details

app = Flask(__name__)
model = pickle.load(open('model2.pkl', 'rb'))
app.secret_key = "detectform"

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

UPLOAD_FOLDER1 = os.path.join(path, 'pdf2img')
if not os.path.isdir(UPLOAD_FOLDER1):
    os.mkdir(UPLOAD_FOLDER1)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1


def Key(dict, key):
    if key in dict.keys():
        print("Present, ", end=" ")
        print("value =", dict[key])
        return dict[key]
    else:
        print("Not present")
        return "Not present"

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/predictfile', methods=['GET', 'POST'])
def predictfile():
    global fn, mn, ln, fn2, mn2, ln2, d, d2, ssn01, ssn02, acc, acc2, s, st, z, z2, st2, c2, s2, c01, ass2, m, sub, sub2
    url1 = request.form['url1']
    url2 = request.form['url2']
    url1 = url1.replace(" ", "%20")
    url2 = url2.replace(" ", "%20")
    a = urllib.request.urlopen("https://docu3c-modelservice.azurewebsites.net/?url=%s" % url1).read().decode('UTF-8')
    data1 = json.loads(a)
    b = urllib.request.urlopen("https://docu3c-modelservice.azurewebsites.net/?url=%s" % url2).read().decode('UTF-8')
    data2 = json.loads(b)

    # print(data1)
    # print(data2)
    fn = Key(data1["details"], "First Name")

    mn = Key(data1["details"], "Middle Name")

    ln = Key(data1["details"], "Last Name")

    d = Key(data1["details"], "DOB")

    ssn01 = Key(data1["details"], "SSN")

    s = Key(data1["details"], "Street")

    c01 = Key(data1["details"], "City")

    st = Key(data1["details"], "State")

    z = Key(data1["details"], "Zip-code")

    acc = Key(data1["details"], "Account No.")

    sub = Key(data1, "Sub Category")

    fn2 = Key(data2["details"], "First Name")

    mn2 = Key(data2["details"], "Middle Name")

    ln2 = Key(data2["details"], "Last Name")

    d2 = Key(data2["details"], "DOB")

    ssn02 = Key(data2["details"], "SSN")

    s2 = Key(data2["details"], "Street")

    c2 = Key(data2["details"], "City")

    st2 = Key(data2["details"], "State")

    z2 = Key(data2["details"], "Zip-code")

    acc2 = Key(data2["details"], "Account No.")

    sub2 = Key(data2, "Sub Category")
    cat = data2["Category"]
    if cat is "Client Account Transfer Form ":
        m = 1
    else:
        m = 0
    ass2 = Key(data2["details"], "List of Assets")

    name1 = fn + " " + mn + " " + ln
    # print(name1)
    name2 = fn2 + " " + mn2 + " " + ln2
    # print(name2)
    c, c1 = count(name1, name2)
    if name1 == "Not present" or name2 == "Not present":
        name = "---"
    else:
        if c >= 2 and c1 >= 2:
            ra = get_ratio(name1, name2)
            feat = [[ra]]
            name = model.predict(feat)
            if name == 1:
                name = "Matched"
            if name == 0:
                name = "Mismatched"
        else:
            name = "Mismatched"

    dob1 = d
    # print(dob1)
    dob2 = d2
    # print(dob2)
    if dob1 == "Not present" or dob2 == "Not present":
        dob = "---"
    else:
        ra1 = get_ratio(dob1, dob2)
        feat = [[ra1]]
        dob = model.predict(feat)
        if dob == 1:
            dob = "Matched"
        if dob == 0:
            dob = "Mismatched"

    ssn1 = ssn01
    ssn2 = ssn02
    # print(ssn1)
    # print(ssn2)
    if ssn1 == "Not present" or ssn2 == "Not present":
        ssn = "---"
    else:
        ra3 = get_ratio(ssn1, ssn2)
        feat = [[ra3]]
        ssn = model.predict(feat)
        if ssn == 1:
            ssn = "Matched"
        if ssn == 0:
            ssn = "Mismatched"

    accno1 = acc
    accno2 = acc2
    # print(accno1)
    # print(accno2)
    if accno1 == "Not present" or accno2 == "Not present":
        accno = "---"
    else:
        ra4 = get_ratio(accno1, accno2)
        feat = [[ra4]]
        accno = model.predict(feat)
        if accno == 1:
            accno = "Matched"
        if accno == 0:
            accno = "Mismatched"

    add1 = s + " " + c01 + " " + st + " " + z
    add2 = s2 + " " + c2 + " " + st2 + " " + z2
    # print(add1)
    # print(add2)
    if add1 == "Not present Not present Not present Not present" or add2 == "Not present Not present Not present Not present":
        add = "---"
    else:
        ra2 = get_ratio(add1, add2)
        feat = [[ra2]]
        add = model.predict(feat)
        if add == 1:
            add = "Matched"
        if add == 0:
            add = "Mismatched"

    if m is 1:
        mutual1 = ass2
        mutual2 = "AHYMX" or "ADNYX" or "GPRIX" or "NSDVX" or "PRIJX" or "VMSXX" or "SGARX" or "ARBIX" or "AWMIX" or "GPGIX" or "BIVIX" or "MSCFX" or "RAIIX" or "IOFIX" or "PTIAX"
        ra4 = get_ratio(mutual1, mutual2)
        feat = [[ra4]]
        mutual = model.predict(feat)
        if mutual == 1:
            mutual = "Yes"
        if mutual == 0:
            mutual = "---"
    else:
        mutual = '---'

    subcat1 = sub
    subcat2 = sub2
    print(subcat1)
    print(subcat2)
    if subcat1 == "Not present" or subcat2 == "Not present":
        subcat = "---"
    else:
        ra5 = get_ratio(subcat1, subcat2)
        feat = [[ra5]]
        subcat = model.predict(feat)
        if subcat == 1:
            subcat = "Matched"
        if subcat == 0:
            subcat = "Mismatched"

    # output = {"Full Name": name, "SSN": ssn, "DOB": dob, "Address": add, "AccountNo": accno, "SubCategory": subcat, "Signature": "---", "DateofSignature": "---", "ViolationofMutualFund": mutual}
    # return output
    return render_template('predict.html', name=name, dob=dob, ssn=ssn, accno=accno, add=add, mutual=mutual,
                           subcat=subcat, sig="---")


if __name__ == "__main__":
    app.run(debug=True)
