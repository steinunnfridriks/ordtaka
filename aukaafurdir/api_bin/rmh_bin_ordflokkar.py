rmhToBin = {
  "nk":"kk", #nafnorð í kk
  "nv":"kvk", #nafnorð í hk
  "nh":"hk", #nafnorð í hk
  "lk":"lo", #lýsingarorð í kk
  "lv":"lo", #lýsingarorð í kvk
  "lh":"lo", #lýsingarorð í hk
  "fa":"fn", #ábendingarfornafn
  "fb":"fn", #óákveðið ábendingarfornafn
  "fe":"fn", #eignarfornafn
  "fo":"fn", #óákveðið fornafn
  "fp":"pfn", #persónufornafn
  "fs":"fn", #spurnarfornafn
  "ft":"fn", #tilvísunarfornafn
  "gk":"gr", #greinir í kk
  "gv":"gr", #greinir í kvk
  "gh":"gr", #greinir í hk
  "tf":"to", #frumtala
  "ta":"[TÖLUSTAFIR]", #ártal eða önnur tala skrifuð með tölustöfum
  "tp":"[TÖLUSTAFIR]", #prósentutölur
  "to":"???", #fjöldatala framan við hundrað eða þúsund
  "sn":"so", #sögn í nafnhætti
  "sb":"so", #sögn í boðhætti
  "sf":"so", #sögn í framsöguhætti
  "sv":"so", #sögn í viðtengingarhætti
  "ss":"so", #sagnbót
  "sl":"so", #sögn í lýsingarhætti nútíðar
  "sþ":"so", #sögn í lýsingarhætti þátíðar
  "aa":"ao", #atviksorð
  "au":"uh", #upphrópun
  "ao":"fs", #atviksorð/forsetning sem stýrir þf
  "aþ":"fs", #atviksorð/forsetning sem stýrir þgf
  "ae":"fs", #atviksorð/forsetning sem stýrir ef
  "as":"[SKAMMSTÖFUN]", #skammstöfun
  "c":"st", #samtenging
  "cn":"nhm", #nafnháttarmerki
  "ct":"st", #tilvísunartenging
  "e":"[ERLENT]", #erlent
  "x":"[ÓGREINT]", #ógreint
  "v":"[NETFANG/VEFFANG]", #netfang/veffang
}


def binOrdflokkur(mark):
  return rmhToBin[mark[:2]]
