import sys
import os
import ssl
import pprint
import re

from opinion import Opinion

TRUST_OID = "1.2.3.4.5.6.7.8"


def get_cert_dict(certname):
    cert_file_name = os.path.join(os.path.dirname(__file__), certname)
    try:
        cert_dict = ssl._ssl._test_decode_cert(cert_file_name)
    except Exception as e:
        print("Error decoding certificate: {0:}".format(e))
    else:
        pass
        # print("Certificate ({0:s}) data:\n".format(certname))
        # pprint.pprint(cert_dict)
    return cert_dict


def string_to_opi(stri):
    ret = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", stri)
    ret = [float(x) for x in ret]
    # print(ret)
    return Opinion(ret)


def find_in_tuple_dict(d, key):
    for x in d:
        if x[0][0] == key:
            return x[0][1]
    return None


def get_subject_op(d):
    subj = d["subject"]
    return string_to_opi(find_in_tuple_dict(subj, TRUST_OID))


def get_issuer_op(d):
    iss = d["issuer"]
    return string_to_opi(find_in_tuple_dict(iss, TRUST_OID))


def calc_trust(wa_KA_b: Opinion, wa_RT_b: Opinion, wb_KA_c: Opinion) -> Opinion:
    return (wa_KA_b & wa_RT_b) * wb_KA_c


def calc_root_cert_trust(d, wa_RT_b):
    iss = d["issuer"]
    subj = d["subject"]
    w_iss = string_to_opi(find_in_tuple_dict(iss, TRUST_OID))
    w_subj = string_to_opi(find_in_tuple_dict(subj, TRUST_OID))
    # print(w_iss, w_subj)
    # print(w_subj.Exp())

    return calc_trust(w_iss, wa_RT_b, w_subj)


if __name__ == "__main__":
    print(
        "Python {0:s} {1:d}bit on {2:s}\n".format(
            " ".join(item.strip() for item in sys.version.split("\n")),
            64 if sys.maxsize > 0x100000000 else 32,
            sys.platform,
        )
    )

    d = get_cert_dict(sys.argv[1])
    print(calc_root_cert_trust(d, Opinion((0.5, 0, 0.5))))
