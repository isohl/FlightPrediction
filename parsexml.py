import writetoKML
newdata = """<marker lat="40.14909" lng="-110.12704" phz="Launch" hgt="5826" tim="090000" ftm="0"/>
<marker lat="40.14509" lng="-110.12191" phz="Ascent" hgt=" 6679" tim="090630" ftm=" 6.50"/>
<marker lat="40.14464" lng="-110.12162" phz="Ascent" hgt=" 6794" tim="090656" ftm=" 6.94"/>
<marker lat="40.14419" lng="-110.12133" phz="Ascent" hgt=" 7254" tim="090722" ftm=" 7.38"/>
<marker lat="40.14374" lng="-110.12103" phz="Ascent" hgt=" 7714" tim="090749" ftm=" 7.82"/>
<marker lat="40.14329" lng="-110.12074" phz="Ascent" hgt=" 8175" tim="090815" ftm=" 8.26"/>
<marker lat="40.14280" lng="-110.12114" phz="Ascent" hgt=" 8635" tim="090843" ftm=" 8.73"/>
<marker lat="40.14231" lng="-110.12155" phz="Ascent" hgt=" 9121" tim="090912" ftm=" 9.20"/>
<marker lat="40.14181" lng="-110.12195" phz="Ascent" hgt=" 9607" tim="090940" ftm=" 9.67"/>
<marker lat="40.14132" lng="-110.12235" phz="Ascent" hgt=" 10094" tim="091008" ftm=" 10.14"/>
<marker lat="40.14095" lng="-110.12343" phz="Ascent" hgt=" 10580" tim="091037" ftm=" 10.63"/>
<marker lat="40.14059" lng="-110.12450" phz="Ascent" hgt=" 11093" tim="091107" ftm=" 11.12"/>
<marker lat="40.14022" lng="-110.12558" phz="Ascent" hgt=" 11605" tim="091136" ftm=" 11.61"/>
<marker lat="40.13985" lng="-110.12665" phz="Ascent" hgt=" 12118" tim="091206" ftm=" 12.10"/>
<marker lat="40.13956" lng="-110.12791" phz="Ascent" hgt=" 12631" tim="091237" ftm=" 12.62"/>
<marker lat="40.13927" lng="-110.12917" phz="Ascent" hgt=" 13172" tim="091308" ftm=" 13.14"/>
<marker lat="40.13898" lng="-110.13044" phz="Ascent" hgt=" 13713" tim="091339" ftm=" 13.66"/>
<marker lat="40.13869" lng="-110.13170" phz="Ascent" hgt=" 14255" tim="091410" ftm=" 14.18"/>
<marker lat="40.13868" lng="-110.13272" phz="Ascent" hgt=" 14796" tim="091443" ftm=" 14.73"/>
<marker lat="40.13866" lng="-110.13374" phz="Ascent" hgt=" 15372" tim="091516" ftm=" 15.28"/>
<marker lat="40.13864" lng="-110.13476" phz="Ascent" hgt=" 15948" tim="091549" ftm=" 15.83"/>
<marker lat="40.13863" lng="-110.13578" phz="Ascent" hgt=" 16523" tim="091622" ftm=" 16.38"/>
<marker lat="40.13866" lng="-110.13612" phz="Ascent" hgt=" 17099" tim="091658" ftm=" 16.97"/>
<marker lat="40.13869" lng="-110.13646" phz="Ascent" hgt=" 17714" tim="091733" ftm=" 17.56"/>
<marker lat="40.13873" lng="-110.13680" phz="Ascent" hgt=" 18330" tim="091809" ftm=" 18.15"/>
<marker lat="40.13876" lng="-110.13714" phz="Ascent" hgt=" 18945" tim="091844" ftm=" 18.74"/>
<marker lat="40.13869" lng="-110.13619" phz="Ascent" hgt=" 19560" tim="091922" ftm=" 19.38"/>
<marker lat="40.13862" lng="-110.13525" phz="Ascent" hgt=" 20226" tim="092001" ftm=" 20.02"/>
<marker lat="40.13854" lng="-110.13430" phz="Ascent" hgt=" 20892" tim="092039" ftm=" 20.66"/>
<marker lat="40.13847" lng="-110.13336" phz="Ascent" hgt=" 21558" tim="092118" ftm=" 21.30"/>
<marker lat="40.13781" lng="-110.13230" phz="Ascent" hgt=" 22224" tim="092200" ftm=" 22.00"/>
<marker lat="40.13714" lng="-110.13124" phz="Ascent" hgt=" 22955" tim="092242" ftm=" 22.70"/>
<marker lat="40.13648" lng="-110.13017" phz="Ascent" hgt=" 23686" tim="092324" ftm=" 23.40"/>
<marker lat="40.13581" lng="-110.12911" phz="Ascent" hgt=" 24416" tim="092406" ftm=" 24.10"/>
<marker lat="40.13452" lng="-110.12763" phz="Ascent" hgt=" 25147" tim="092452" ftm=" 24.87"/>
<marker lat="40.13322" lng="-110.12615" phz="Ascent" hgt=" 25956" tim="092538" ftm=" 25.64"/>
<marker lat="40.13193" lng="-110.12467" phz="Ascent" hgt=" 26765" tim="092624" ftm=" 26.41"/>
<marker lat="40.13064" lng="-110.12319" phz="Ascent" hgt=" 27573" tim="092710" ftm=" 27.18"/>
<marker lat="40.12994" lng="-110.12117" phz="Ascent" hgt=" 28382" tim="092736" ftm=" 27.61"/>
<marker lat="40.12925" lng="-110.11915" phz="Ascent" hgt=" 28836" tim="092803" ftm=" 28.05"/>
<marker lat="40.12856" lng="-110.11714" phz="Ascent" hgt=" 29291" tim="092828" ftm=" 28.48"/>
<marker lat="40.12786" lng="-110.11512" phz="Ascent" hgt=" 29745" tim="092855" ftm=" 28.92"/>
<marker lat="40.12717" lng="-110.11310" phz="Ascent" hgt=" 30200" tim="092921" ftm=" 29.35"/>
<marker lat="40.12648" lng="-110.11109" phz="Ascent" hgt=" 30654" tim="092946" ftm=" 29.78"/>
<marker lat="40.12578" lng="-110.10907" phz="Ascent" hgt=" 31108" tim="093013" ftm=" 30.22"/>
<marker lat="40.12509" lng="-110.10705" phz="Ascent" hgt=" 31563" tim="093039" ftm=" 30.65"/>
<marker lat="40.12417" lng="-110.10317" phz="Ascent" hgt=" 32017" tim="093109" ftm=" 31.15"/>
<marker lat="40.12325" lng="-110.09928" phz="Ascent" hgt=" 32537" tim="093139" ftm=" 31.65"/>
<marker lat="40.12233" lng="-110.09539" phz="Ascent" hgt=" 33057" tim="093209" ftm=" 32.15"/>
<marker lat="40.12141" lng="-110.09151" phz="Ascent" hgt=" 33577" tim="093239" ftm=" 32.65"/>
<marker lat="40.12049" lng="-110.08763" phz="Ascent" hgt=" 34097" tim="093309" ftm=" 33.15"/>
<marker lat="40.11957" lng="-110.08374" phz="Ascent" hgt=" 34617" tim="093339" ftm=" 33.65"/>
<marker lat="40.11864" lng="-110.07986" phz="Ascent" hgt=" 35137" tim="093409" ftm=" 34.15"/>
<marker lat="40.11772" lng="-110.07597" phz="Ascent" hgt=" 35657" tim="093439" ftm=" 34.65"/>
<marker lat="40.11716" lng="-110.07207" phz="Ascent" hgt=" 36177" tim="093513" ftm=" 35.23"/>
<marker lat="40.11660" lng="-110.06817" phz="Ascent" hgt=" 36788" tim="093548" ftm=" 35.81"/>
<marker lat="40.11604" lng="-110.06427" phz="Ascent" hgt=" 37398" tim="093623" ftm=" 36.39"/>
<marker lat="40.11548" lng="-110.06038" phz="Ascent" hgt=" 38008" tim="093658" ftm=" 36.97"/>
<marker lat="40.11492" lng="-110.05648" phz="Ascent" hgt=" 38618" tim="093733" ftm=" 37.55"/>
<marker lat="40.11436" lng="-110.05258" phz="Ascent" hgt=" 39229" tim="093807" ftm=" 38.13"/>
<marker lat="40.11380" lng="-110.04868" phz="Ascent" hgt=" 39839" tim="093842" ftm=" 38.71"/>
<marker lat="40.11324" lng="-110.04479" phz="Ascent" hgt=" 40449" tim="093917" ftm=" 39.29"/>
<marker lat="40.11421" lng="-110.04018" phz="Ascent" hgt=" 41059" tim="094000" ftm=" 40.01"/>
<marker lat="40.11517" lng="-110.03557" phz="Ascent" hgt=" 41810" tim="094043" ftm=" 40.73"/>
<marker lat="40.11614" lng="-110.03096" phz="Ascent" hgt=" 42561" tim="094127" ftm=" 41.45"/>
<marker lat="40.11711" lng="-110.02636" phz="Ascent" hgt=" 43312" tim="094210" ftm=" 42.17"/>
<marker lat="40.11807" lng="-110.02175" phz="Ascent" hgt=" 44063" tim="094253" ftm=" 42.89"/>
<marker lat="40.11904" lng="-110.01714" phz="Ascent" hgt=" 44814" tim="094336" ftm=" 43.61"/>
<marker lat="40.12000" lng="-110.01254" phz="Ascent" hgt=" 45565" tim="094419" ftm=" 44.33"/>
<marker lat="40.12097" lng="-110.00794" phz="Ascent" hgt=" 46316" tim="094503" ftm=" 45.05"/>
<marker lat="40.12337" lng="-110.00403" phz="Ascent" hgt=" 47066" tim="094531" ftm=" 45.53"/>
<marker lat="40.12577" lng="-110.00013" phz="Ascent" hgt=" 47567" tim="094600" ftm=" 46.01"/>
<marker lat="40.12817" lng="-109.99623" phz="Ascent" hgt=" 48067" tim="094629" ftm=" 46.49"/>
<marker lat="40.13058" lng="-109.99232" phz="Ascent" hgt=" 48567" tim="094658" ftm=" 46.97"/>
<marker lat="40.13298" lng="-109.98842" phz="Ascent" hgt=" 49068" tim="094727" ftm=" 47.45"/>
<marker lat="40.13537" lng="-109.98452" phz="Ascent" hgt=" 49568" tim="094755" ftm=" 47.93"/>
<marker lat="40.13778" lng="-109.98061" phz="Ascent" hgt=" 50068" tim="094824" ftm=" 48.41"/>
<marker lat="40.14018" lng="-109.97670" phz="Ascent" hgt=" 50569" tim="094853" ftm=" 48.89"/>
<marker lat="40.14257" lng="-109.97280" phz="Ascent" hgt=" 51069" tim="094922" ftm=" 49.37"/>
<marker lat="40.14498" lng="-109.96889" phz="Ascent" hgt=" 51569" tim="094951" ftm=" 49.85"/>
<marker lat="40.14738" lng="-109.96499" phz="Ascent" hgt=" 52070" tim="095019" ftm=" 50.33"/>
<marker lat="40.14977" lng="-109.96109" phz="Ascent" hgt=" 52570" tim="095048" ftm=" 50.81"/>
<marker lat="40.15218" lng="-109.95718" phz="Ascent" hgt=" 53070" tim="095117" ftm=" 51.29"/>
<marker lat="40.15458" lng="-109.95327" phz="Ascent" hgt=" 53571" tim="095146" ftm=" 51.77"/>
<marker lat="40.15697" lng="-109.94937" phz="Ascent" hgt=" 54071" tim="095215" ftm=" 52.25"/>
<marker lat="40.15937" lng="-109.94546" phz="Ascent" hgt=" 54571" tim="095243" ftm=" 52.73"/>
<marker lat="40.16079" lng="-109.94458" phz="Ascent" hgt=" 55072" tim="095308" ftm=" 53.14"/>
<marker lat="40.16220" lng="-109.94370" phz="Ascent" hgt=" 55504" tim="095333" ftm=" 53.55"/>
<marker lat="40.16361" lng="-109.94282" phz="Ascent" hgt=" 55936" tim="095357" ftm=" 53.96"/>
<marker lat="40.16501" lng="-109.94195" phz="Ascent" hgt=" 56368" tim="095422" ftm=" 54.37"/>
<marker lat="40.16642" lng="-109.94107" phz="Ascent" hgt=" 56799" tim="095446" ftm=" 54.78"/>
<marker lat="40.16783" lng="-109.94020" phz="Ascent" hgt=" 57231" tim="095511" ftm=" 55.19"/>
<marker lat="40.16925" lng="-109.93932" phz="Ascent" hgt=" 57663" tim="095536" ftm=" 55.60"/>
<marker lat="40.17066" lng="-109.93844" phz="Ascent" hgt=" 58095" tim="095600" ftm=" 56.01"/>
<marker lat="40.17207" lng="-109.93756" phz="Ascent" hgt=" 58527" tim="095625" ftm=" 56.42"/>
<marker lat="40.17348" lng="-109.93669" phz="Ascent" hgt=" 58959" tim="095649" ftm=" 56.83"/>
<marker lat="40.17489" lng="-109.93581" phz="Ascent" hgt=" 59391" tim="095714" ftm=" 57.24"/>
<marker lat="40.17630" lng="-109.93493" phz="Ascent" hgt=" 59823" tim="095739" ftm=" 57.65"/>
<marker lat="40.17771" lng="-109.93405" phz="Ascent" hgt=" 60255" tim="095803" ftm=" 58.06"/>
<marker lat="40.17912" lng="-109.93318" phz="Ascent" hgt=" 60687" tim="095828" ftm=" 58.47"/>
<marker lat="40.18053" lng="-109.93230" phz="Ascent" hgt=" 61119" tim="095852" ftm=" 58.88"/>
<marker lat="40.18194" lng="-109.93142" phz="Ascent" hgt=" 61551" tim="095917" ftm=" 59.29"/>
<marker lat="40.18335" lng="-109.93054" phz="Ascent" hgt=" 61983" tim="095942" ftm=" 59.70"/>
<marker lat="40.18476" lng="-109.92966" phz="Ascent" hgt=" 62415" tim="100006" ftm=" 60.11"/>
<marker lat="40.18617" lng="-109.92879" phz="Ascent" hgt=" 62847" tim="100031" ftm=" 60.52"/>
<marker lat="40.18758" lng="-109.92791" phz="Ascent" hgt=" 63279" tim="100055" ftm=" 60.93"/>
<marker lat="40.18899" lng="-109.92703" phz="Ascent" hgt=" 63711" tim="100120" ftm=" 61.34"/>
<marker lat="40.19040" lng="-109.92616" phz="Ascent" hgt=" 64142" tim="100145" ftm=" 61.75"/>
<marker lat="40.19181" lng="-109.92528" phz="Ascent" hgt=" 64574" tim="100209" ftm=" 62.16"/>
<marker lat="40.19322" lng="-109.92440" phz="Ascent" hgt=" 65006" tim="100234" ftm=" 62.57"/>
<marker lat="40.19463" lng="-109.92352" phz="Ascent" hgt=" 65438" tim="100258" ftm=" 62.98"/>
<marker lat="40.19604" lng="-109.92264" phz="Ascent" hgt=" 65870" tim="100323" ftm=" 63.39"/>
<marker lat="40.19745" lng="-109.92177" phz="Ascent" hgt=" 66302" tim="100348" ftm=" 63.80"/>
<marker lat="40.19886" lng="-109.92089" phz="Ascent" hgt=" 66734" tim="100412" ftm=" 64.21"/>
<marker lat="40.20027" lng="-109.92001" phz="Ascent" hgt=" 67166" tim="100437" ftm=" 64.62"/>
<marker lat="40.20168" lng="-109.91913" phz="Ascent" hgt=" 67598" tim="100501" ftm=" 65.03"/>
<marker lat="40.20309" lng="-109.91825" phz="Ascent" hgt=" 68030" tim="100526" ftm=" 65.44"/>
<marker lat="40.20450" lng="-109.91738" phz="Ascent" hgt=" 68462" tim="100551" ftm=" 65.85"/>
<marker lat="40.20455" lng="-109.91946" phz="Ascent" hgt=" 68894" tim="100625" ftm=" 66.43"/>
<marker lat="40.20461" lng="-109.92154" phz="Ascent" hgt=" 69499" tim="100700" ftm=" 67.01"/>
<marker lat="40.20466" lng="-109.92363" phz="Ascent" hgt=" 70104" tim="100735" ftm=" 67.59"/>
<marker lat="40.20471" lng="-109.92571" phz="Ascent" hgt=" 70709" tim="100810" ftm=" 68.17"/>
<marker lat="40.20476" lng="-109.92779" phz="Ascent" hgt=" 71314" tim="100845" ftm=" 68.75"/>
<marker lat="40.20481" lng="-109.92988" phz="Ascent" hgt=" 71919" tim="100919" ftm=" 69.33"/>
<marker lat="40.20486" lng="-109.93196" phz="Ascent" hgt=" 72525" tim="100954" ftm=" 69.91"/>
<marker lat="40.20491" lng="-109.93405" phz="Ascent" hgt=" 73130" tim="101029" ftm=" 70.49"/>
<marker lat="40.20496" lng="-109.93613" phz="Ascent" hgt=" 73735" tim="101104" ftm=" 71.07"/>
<marker lat="40.20501" lng="-109.93821" phz="Ascent" hgt=" 74340" tim="101139" ftm=" 71.65"/>
<marker lat="40.20506" lng="-109.94030" phz="Ascent" hgt=" 74945" tim="101213" ftm=" 72.23"/>
<marker lat="40.20511" lng="-109.94238" phz="Ascent" hgt=" 75550" tim="101248" ftm=" 72.81"/>
<marker lat="40.20516" lng="-109.94446" phz="Ascent" hgt=" 76155" tim="101323" ftm=" 73.39"/>
<marker lat="40.20521" lng="-109.94655" phz="Ascent" hgt=" 76760" tim="101358" ftm=" 73.97"/>
<marker lat="40.20526" lng="-109.94864" phz="Ascent" hgt=" 77365" tim="101433" ftm=" 74.55"/>
<marker lat="40.20531" lng="-109.95072" phz="Ascent" hgt=" 77971" tim="101507" ftm=" 75.13"/>
<marker lat="40.20537" lng="-109.95280" phz="Ascent" hgt=" 78576" tim="101542" ftm=" 75.71"/>
<marker lat="40.20542" lng="-109.95489" phz="Ascent" hgt=" 79181" tim="101617" ftm=" 76.29"/>
<marker lat="40.20546" lng="-109.95697" phz="Ascent" hgt=" 79786" tim="101652" ftm=" 76.87"/>
<marker lat="40.20552" lng="-109.95905" phz="Ascent" hgt=" 80391" tim="101727" ftm=" 77.45"/>
<marker lat="40.20557" lng="-109.96114" phz="Ascent" hgt=" 80996" tim="101801" ftm=" 78.03"/>
<marker lat="40.20562" lng="-109.96322" phz="Ascent" hgt=" 81601" tim="101836" ftm=" 78.61"/>
<marker lat="40.20567" lng="-109.96530" phz="Ascent" hgt=" 82206" tim="101911" ftm=" 79.19"/>
<marker lat="40.20572" lng="-109.96739" phz="Ascent" hgt=" 82811" tim="101946" ftm=" 79.77"/>
<marker lat="40.20577" lng="-109.96948" phz="Ascent" hgt=" 83416" tim="102021" ftm=" 80.35"/>
<marker lat="40.20582" lng="-109.97156" phz="Ascent" hgt=" 84022" tim="102055" ftm=" 80.93"/>
<marker lat="40.20587" lng="-109.97364" phz="Ascent" hgt=" 84627" tim="102130" ftm=" 81.51"/>
<marker lat="40.20592" lng="-109.97573" phz="Ascent" hgt=" 85232" tim="102205" ftm=" 82.09"/>
<marker lat="40.20597" lng="-109.97781" phz="Ascent" hgt=" 85837" tim="102240" ftm=" 82.67"/>
<marker lat="40.20602" lng="-109.97989" phz="Ascent" hgt=" 86442" tim="102315" ftm=" 83.25"/>
<marker lat="40.20607" lng="-109.98198" phz="Ascent" hgt=" 87047" tim="102349" ftm=" 83.83"/>
<marker lat="40.20612" lng="-109.98406" phz="Ascent" hgt=" 87652" tim="102424" ftm=" 84.41"/>
<marker lat="40.20657" lng="-109.99125" phz="Ascent" hgt=" 88257" tim="102510" ftm=" 85.18"/>
<marker lat="40.20702" lng="-109.99846" phz="Ascent" hgt=" 89064" tim="102557" ftm=" 85.95"/>
<marker lat="40.20747" lng="-110.00565" phz="Ascent" hgt=" 89872" tim="102643" ftm=" 86.72"/>
<marker lat="40.20792" lng="-110.01285" phz="Ascent" hgt=" 90679" tim="102729" ftm=" 87.49"/>
<marker lat="40.20818" lng="-110.01714" phz="Ascent" hgt=" 91486" tim="102757" ftm=" 87.95"/>
<marker lat="40.20845" lng="-110.02142" phz="Ascent" hgt=" 91967" tim="102824" ftm=" 88.41"/>
<marker lat="40.20872" lng="-110.02570" phz="Ascent" hgt=" 92447" tim="102852" ftm=" 88.87"/>
<marker lat="40.20899" lng="-110.02999" phz="Ascent" hgt=" 92928" tim="102919" ftm=" 89.33"/>
<marker lat="40.20925" lng="-110.03428" phz="Ascent" hgt=" 93409" tim="102947" ftm=" 89.79"/>
<marker lat="40.20952" lng="-110.03857" phz="Ascent" hgt=" 93890" tim="103015" ftm=" 90.25"/>
<marker lat="40.20979" lng="-110.04286" phz="Ascent" hgt=" 94371" tim="103042" ftm=" 90.71"/>
<marker lat="40.21005" lng="-110.04715" phz="Ascent" hgt=" 94852" tim="103110" ftm=" 91.17"/>
<marker lat="40.21032" lng="-110.05143" phz="Ascent" hgt=" 95333" tim="103137" ftm=" 91.63"/>
<marker lat="40.21059" lng="-110.05572" phz="Ascent" hgt=" 95813" tim="103205" ftm=" 92.09"/>
<marker lat="40.21085" lng="-110.06000" phz="Ascent" hgt=" 96294" tim="103233" ftm=" 92.55"/>
<marker lat="40.21112" lng="-110.06429" phz="Ascent" hgt=" 96775" tim="103300" ftm=" 93.01"/>
<marker lat="40.21138" lng="-110.06858" phz="Ascent" hgt=" 97256" tim="103328" ftm=" 93.47"/>
<marker lat="40.21153" lng="-110.07093" phz="Burst" hgt=" 97737" tim="103343" ftm=" 93.72"/>
<marker lat="40.21154" lng="-110.07108" phz="Descent" hgt=" 97737" tim="103344" ftm=" 93.74"/>
<marker lat="40.21156" lng="-110.07137" phz="Descent" hgt=" 97256" tim="103346" ftm=" 93.77"/>
<marker lat="40.21157" lng="-110.07166" phz="Descent" hgt=" 96775" tim="103348" ftm=" 93.80"/>
<marker lat="40.21159" lng="-110.07195" phz="Descent" hgt=" 96294" tim="103349" ftm=" 93.83"/>
<marker lat="40.21161" lng="-110.07224" phz="Descent" hgt=" 95813" tim="103351" ftm=" 93.86"/>
<marker lat="40.21163" lng="-110.07256" phz="Descent" hgt=" 95333" tim="103353" ftm=" 93.89"/>
<marker lat="40.21165" lng="-110.07285" phz="Descent" hgt=" 94852" tim="103355" ftm=" 93.92"/>
<marker lat="40.21167" lng="-110.07316" phz="Descent" hgt=" 94371" tim="103357" ftm=" 93.95"/>
<marker lat="40.21169" lng="-110.07346" phz="Descent" hgt=" 93890" tim="103358" ftm=" 93.98"/>
<marker lat="40.21171" lng="-110.07378" phz="Descent" hgt=" 93409" tim="103400" ftm=" 94.01"/>
<marker lat="40.21172" lng="-110.07409" phz="Descent" hgt=" 92928" tim="103402" ftm=" 94.04"/>
<marker lat="40.21174" lng="-110.07441" phz="Descent" hgt=" 92447" tim="103404" ftm=" 94.07"/>
<marker lat="40.21176" lng="-110.07473" phz="Descent" hgt=" 91967" tim="103406" ftm=" 94.10"/>
<marker lat="40.21178" lng="-110.07506" phz="Descent" hgt=" 91486" tim="103408" ftm=" 94.14"/>
<marker lat="40.21182" lng="-110.07561" phz="Descent" hgt=" 90679" tim="103412" ftm=" 94.20"/>
<marker lat="40.21185" lng="-110.07619" phz="Descent" hgt=" 89872" tim="103415" ftm=" 94.26"/>
<marker lat="40.21189" lng="-110.07676" phz="Descent" hgt=" 89064" tim="103419" ftm=" 94.32"/>
<marker lat="40.21193" lng="-110.07736" phz="Descent" hgt=" 88257" tim="103422" ftm=" 94.38"/>
<marker lat="40.21193" lng="-110.07753" phz="Descent" hgt=" 87652" tim="103425" ftm=" 94.43"/>
<marker lat="40.21193" lng="-110.07771" phz="Descent" hgt=" 87047" tim="103428" ftm=" 94.48"/>
<marker lat="40.21194" lng="-110.07788" phz="Descent" hgt=" 86442" tim="103431" ftm=" 94.53"/>
<marker lat="40.21194" lng="-110.07807" phz="Descent" hgt=" 85837" tim="103434" ftm=" 94.58"/>
<marker lat="40.21195" lng="-110.07825" phz="Descent" hgt=" 85232" tim="103437" ftm=" 94.63"/>
<marker lat="40.21195" lng="-110.07844" phz="Descent" hgt=" 84627" tim="103440" ftm=" 94.68"/>
<marker lat="40.21196" lng="-110.07862" phz="Descent" hgt=" 84022" tim="103443" ftm=" 94.73"/>
<marker lat="40.21196" lng="-110.07883" phz="Descent" hgt=" 83416" tim="103447" ftm=" 94.79"/>
<marker lat="40.21196" lng="-110.07902" phz="Descent" hgt=" 82811" tim="103450" ftm=" 94.84"/>
<marker lat="40.21197" lng="-110.07922" phz="Descent" hgt=" 82206" tim="103453" ftm=" 94.89"/>
<marker lat="40.21197" lng="-110.07941" phz="Descent" hgt=" 81601" tim="103456" ftm=" 94.94"/>
<marker lat="40.21198" lng="-110.07962" phz="Descent" hgt=" 80996" tim="103500" ftm=" 95.00"/>
<marker lat="40.21198" lng="-110.07982" phz="Descent" hgt=" 80391" tim="103503" ftm=" 95.06"/>
<marker lat="40.21199" lng="-110.08003" phz="Descent" hgt=" 79786" tim="103507" ftm=" 95.12"/>
<marker lat="40.21199" lng="-110.08024" phz="Descent" hgt=" 79181" tim="103510" ftm=" 95.18"/>
<marker lat="40.21200" lng="-110.08049" phz="Descent" hgt=" 78576" tim="103515" ftm=" 95.25"/>
<marker lat="40.21200" lng="-110.08071" phz="Descent" hgt=" 77971" tim="103518" ftm=" 95.31"/>
<marker lat="40.21201" lng="-110.08093" phz="Descent" hgt=" 77365" tim="103522" ftm=" 95.37"/>
<marker lat="40.21201" lng="-110.08115" phz="Descent" hgt=" 76760" tim="103525" ftm=" 95.43"/>
<marker lat="40.21202" lng="-110.08138" phz="Descent" hgt=" 76155" tim="103529" ftm=" 95.49"/>
<marker lat="40.21202" lng="-110.08160" phz="Descent" hgt=" 75550" tim="103533" ftm=" 95.55"/>
<marker lat="40.21203" lng="-110.08183" phz="Descent" hgt=" 74945" tim="103536" ftm=" 95.61"/>
<marker lat="40.21204" lng="-110.08207" phz="Descent" hgt=" 74340" tim="103540" ftm=" 95.67"/>
<marker lat="40.21204" lng="-110.08232" phz="Descent" hgt=" 73735" tim="103544" ftm=" 95.74"/>
<marker lat="40.21205" lng="-110.08256" phz="Descent" hgt=" 73130" tim="103548" ftm=" 95.81"/>
<marker lat="40.21205" lng="-110.08280" phz="Descent" hgt=" 72525" tim="103552" ftm=" 95.88"/>
<marker lat="40.21206" lng="-110.08305" phz="Descent" hgt=" 71919" tim="103557" ftm=" 95.95"/>
<marker lat="40.21206" lng="-110.08331" phz="Descent" hgt=" 71314" tim="103601" ftm=" 96.02"/>
<marker lat="40.21207" lng="-110.08356" phz="Descent" hgt=" 70709" tim="103605" ftm=" 96.09"/>
<marker lat="40.21208" lng="-110.08382" phz="Descent" hgt=" 70104" tim="103609" ftm=" 96.16"/>
<marker lat="40.21208" lng="-110.08407" phz="Descent" hgt=" 69499" tim="103613" ftm=" 96.23"/>
<marker lat="40.21209" lng="-110.08435" phz="Descent" hgt=" 68894" tim="103618" ftm=" 96.31"/>
<marker lat="40.21227" lng="-110.08424" phz="Descent" hgt=" 68462" tim="103621" ftm=" 96.36"/>
<marker lat="40.21245" lng="-110.08413" phz="Descent" hgt=" 68030" tim="103624" ftm=" 96.41"/>
<marker lat="40.21263" lng="-110.08401" phz="Descent" hgt=" 67598" tim="103627" ftm=" 96.46"/>
<marker lat="40.21282" lng="-110.08390" phz="Descent" hgt=" 67166" tim="103631" ftm=" 96.52"/>
<marker lat="40.21300" lng="-110.08378" phz="Descent" hgt=" 66734" tim="103634" ftm=" 96.57"/>
<marker lat="40.21319" lng="-110.08366" phz="Descent" hgt=" 66302" tim="103637" ftm=" 96.63"/>
<marker lat="40.21338" lng="-110.08355" phz="Descent" hgt=" 65870" tim="103641" ftm=" 96.69"/>
<marker lat="40.21359" lng="-110.08342" phz="Descent" hgt=" 65438" tim="103645" ftm=" 96.75"/>
<marker lat="40.21378" lng="-110.08330" phz="Descent" hgt=" 65006" tim="103648" ftm=" 96.81"/>
<marker lat="40.21397" lng="-110.08318" phz="Descent" hgt=" 64574" tim="103652" ftm=" 96.87"/>
<marker lat="40.21417" lng="-110.08306" phz="Descent" hgt=" 64142" tim="103655" ftm=" 96.93"/>
<marker lat="40.21438" lng="-110.08293" phz="Descent" hgt=" 63711" tim="103659" ftm=" 96.99"/>
<marker lat="40.21458" lng="-110.08281" phz="Descent" hgt=" 63279" tim="103703" ftm=" 97.05"/>
<marker lat="40.21478" lng="-110.08268" phz="Descent" hgt=" 62847" tim="103706" ftm=" 97.11"/>
<marker lat="40.21498" lng="-110.08255" phz="Descent" hgt=" 62415" tim="103710" ftm=" 97.17"/>
<marker lat="40.21522" lng="-110.08240" phz="Descent" hgt=" 61983" tim="103714" ftm=" 97.24"/>
<marker lat="40.21543" lng="-110.08228" phz="Descent" hgt=" 61551" tim="103718" ftm=" 97.30"/>
<marker lat="40.21564" lng="-110.08214" phz="Descent" hgt=" 61119" tim="103721" ftm=" 97.36"/>
<marker lat="40.21586" lng="-110.08201" phz="Descent" hgt=" 60687" tim="103725" ftm=" 97.42"/>
<marker lat="40.21608" lng="-110.08188" phz="Descent" hgt=" 60255" tim="103728" ftm=" 97.48"/>
<marker lat="40.21629" lng="-110.08174" phz="Descent" hgt=" 59823" tim="103732" ftm=" 97.54"/>
<marker lat="40.21652" lng="-110.08160" phz="Descent" hgt=" 59391" tim="103736" ftm=" 97.60"/>
<marker lat="40.21674" lng="-110.08147" phz="Descent" hgt=" 58959" tim="103739" ftm=" 97.66"/>
<marker lat="40.21697" lng="-110.08132" phz="Descent" hgt=" 58527" tim="103743" ftm=" 97.73"/>
<marker lat="40.21720" lng="-110.08118" phz="Descent" hgt=" 58095" tim="103748" ftm=" 97.80"/>
<marker lat="40.21743" lng="-110.08104" phz="Descent" hgt=" 57663" tim="103752" ftm=" 97.87"/>
<marker lat="40.21766" lng="-110.08089" phz="Descent" hgt=" 57231" tim="103756" ftm=" 97.94"/>
<marker lat="40.21790" lng="-110.08075" phz="Descent" hgt=" 56799" tim="103800" ftm=" 98.01"/>
<marker lat="40.21813" lng="-110.08060" phz="Descent" hgt=" 56368" tim="103804" ftm=" 98.08"/>
<marker lat="40.21837" lng="-110.08045" phz="Descent" hgt=" 55936" tim="103809" ftm=" 98.15"/>
<marker lat="40.21861" lng="-110.08031" phz="Descent" hgt=" 55504" tim="103813" ftm=" 98.22"/>
<marker lat="40.21887" lng="-110.08014" phz="Descent" hgt=" 55072" tim="103818" ftm=" 98.30"/>
<marker lat="40.21929" lng="-110.07947" phz="Descent" hgt=" 54571" tim="103822" ftm=" 98.38"/>
<marker lat="40.21972" lng="-110.07877" phz="Descent" hgt=" 54071" tim="103827" ftm=" 98.46"/>
<marker lat="40.22014" lng="-110.07808" phz="Descent" hgt=" 53571" tim="103832" ftm=" 98.54"/>
<marker lat="40.22059" lng="-110.07736" phz="Descent" hgt=" 53070" tim="103837" ftm=" 98.63"/>
<marker lat="40.22102" lng="-110.07665" phz="Descent" hgt=" 52570" tim="103843" ftm=" 98.72"/>
<marker lat="40.22147" lng="-110.07593" phz="Descent" hgt=" 52070" tim="103848" ftm=" 98.81"/>
<marker lat="40.22191" lng="-110.07520" phz="Descent" hgt=" 51569" tim="103854" ftm=" 98.90"/>
<marker lat="40.22240" lng="-110.07441" phz="Descent" hgt=" 51069" tim="103900" ftm=" 99.00"/>
<marker lat="40.22286" lng="-110.07367" phz="Descent" hgt=" 50569" tim="103905" ftm=" 99.09"/>
<marker lat="40.22332" lng="-110.07291" phz="Descent" hgt=" 50068" tim="103910" ftm=" 99.18"/>
<marker lat="40.22379" lng="-110.07216" phz="Descent" hgt=" 49568" tim="103916" ftm=" 99.27"/>
<marker lat="40.22427" lng="-110.07137" phz="Descent" hgt=" 49068" tim="103922" ftm=" 99.37"/>
<marker lat="40.22475" lng="-110.07059" phz="Descent" hgt=" 48567" tim="103928" ftm=" 99.47"/>
<marker lat="40.22524" lng="-110.06980" phz="Descent" hgt=" 48067" tim="103934" ftm=" 99.57"/>
<marker lat="40.22573" lng="-110.06901" phz="Descent" hgt=" 47567" tim="103940" ftm=" 99.67"/>
<marker lat="40.22628" lng="-110.06811" phz="Descent" hgt=" 47066" tim="103946" ftm=" 99.78"/>
<marker lat="40.22648" lng="-110.06714" phz="Descent" hgt=" 46316" tim="103955" ftm=" 99.93"/>
<marker lat="40.22669" lng="-110.06614" phz="Descent" hgt=" 45565" tim="104005" ftm="100.09"/>
<marker lat="40.22690" lng="-110.06514" phz="Descent" hgt=" 44814" tim="104015" ftm="100.25"/>
<marker lat="40.22712" lng="-110.06407" phz="Descent" hgt=" 44063" tim="104025" ftm="100.42"/>
<marker lat="40.22734" lng="-110.06303" phz="Descent" hgt=" 43312" tim="104034" ftm="100.58"/>
<marker lat="40.22757" lng="-110.06196" phz="Descent" hgt=" 42561" tim="104045" ftm="100.75"/>
<marker lat="40.22779" lng="-110.06089" phz="Descent" hgt=" 41810" tim="104055" ftm="100.92"/>
<marker lat="40.22805" lng="-110.05967" phz="Descent" hgt=" 41059" tim="104106" ftm="101.11"/>
<marker lat="40.22791" lng="-110.05874" phz="Descent" hgt=" 40449" tim="104115" ftm="101.25"/>
<marker lat="40.22778" lng="-110.05778" phz="Descent" hgt=" 39839" tim="104123" ftm="101.39"/>
<marker lat="40.22764" lng="-110.05682" phz="Descent" hgt=" 39229" tim="104131" ftm="101.53"/>
<marker lat="40.22749" lng="-110.05581" phz="Descent" hgt=" 38618" tim="104140" ftm="101.68"/>
<marker lat="40.22735" lng="-110.05482" phz="Descent" hgt=" 38008" tim="104149" ftm="101.83"/>
<marker lat="40.22720" lng="-110.05381" phz="Descent" hgt=" 37398" tim="104158" ftm="101.98"/>
<marker lat="40.22706" lng="-110.05279" phz="Descent" hgt=" 36788" tim="104207" ftm="102.13"/>
<marker lat="40.22689" lng="-110.05164" phz="Descent" hgt=" 36177" tim="104218" ftm="102.30"/>
<marker lat="40.22665" lng="-110.05061" phz="Descent" hgt=" 35657" tim="104225" ftm="102.43"/>
<marker lat="40.22640" lng="-110.04955" phz="Descent" hgt=" 35137" tim="104234" ftm="102.57"/>
<marker lat="40.22615" lng="-110.04849" phz="Descent" hgt=" 34617" tim="104242" ftm="102.71"/>
<marker lat="40.22588" lng="-110.04738" phz="Descent" hgt=" 34097" tim="104251" ftm="102.85"/>
<marker lat="40.22563" lng="-110.04630" phz="Descent" hgt=" 33577" tim="104259" ftm="102.99"/>
<marker lat="40.22536" lng="-110.04519" phz="Descent" hgt=" 33057" tim="104307" ftm="103.13"/>
<marker lat="40.22510" lng="-110.04408" phz="Descent" hgt=" 32537" tim="104316" ftm="103.27"/>
<marker lat="40.22480" lng="-110.04282" phz="Descent" hgt=" 32017" tim="104325" ftm="103.43"/>
<marker lat="40.22460" lng="-110.04224" phz="Descent" hgt=" 31563" tim="104333" ftm="103.56"/>
<marker lat="40.22439" lng="-110.04163" phz="Descent" hgt=" 31108" tim="104341" ftm="103.69"/>
<marker lat="40.22419" lng="-110.04103" phz="Descent" hgt=" 30654" tim="104349" ftm="103.82"/>
<marker lat="40.22397" lng="-110.04041" phz="Descent" hgt=" 30200" tim="104357" ftm="103.95"/>
<marker lat="40.22376" lng="-110.03980" phz="Descent" hgt=" 29745" tim="104404" ftm="104.08"/>
<marker lat="40.22355" lng="-110.03917" phz="Descent" hgt=" 29291" tim="104412" ftm="104.21"/>
<marker lat="40.22333" lng="-110.03855" phz="Descent" hgt=" 28836" tim="104420" ftm="104.34"/>
<marker lat="40.22309" lng="-110.03784" phz="Descent" hgt=" 28382" tim="104429" ftm="104.49"/>
<marker lat="40.22267" lng="-110.03737" phz="Descent" hgt=" 27573" tim="104444" ftm="104.74"/>
<marker lat="40.22224" lng="-110.03687" phz="Descent" hgt=" 26765" tim="104500" ftm="105.00"/>
<marker lat="40.22181" lng="-110.03638" phz="Descent" hgt=" 25956" tim="104515" ftm="105.26"/>
<marker lat="40.22133" lng="-110.03583" phz="Descent" hgt=" 25147" tim="104533" ftm="105.55"/>
<marker lat="40.22110" lng="-110.03546" phz="Descent" hgt=" 24416" tim="104547" ftm="105.79"/>
<marker lat="40.22086" lng="-110.03508" phz="Descent" hgt=" 23686" tim="104602" ftm="106.04"/>
<marker lat="40.22062" lng="-110.03471" phz="Descent" hgt=" 22955" tim="104617" ftm="106.29"/>
<marker lat="40.22036" lng="-110.03428" phz="Descent" hgt=" 22224" tim="104634" ftm="106.57"/>
<marker lat="40.22033" lng="-110.03394" phz="Descent" hgt=" 21558" tim="104648" ftm="106.80"/>
<marker lat="40.22031" lng="-110.03358" phz="Descent" hgt=" 20892" tim="104702" ftm="107.04"/>
<marker lat="40.22028" lng="-110.03322" phz="Descent" hgt=" 20226" tim="104716" ftm="107.28"/>
<marker lat="40.22025" lng="-110.03283" phz="Descent" hgt=" 19560" tim="104733" ftm="107.55"/>
<marker lat="40.22026" lng="-110.03296" phz="Descent" hgt=" 18945" tim="104746" ftm="107.78"/>
<marker lat="40.22028" lng="-110.03310" phz="Descent" hgt=" 18330" tim="104801" ftm="108.02"/>
<marker lat="40.22029" lng="-110.03323" phz="Descent" hgt=" 17714" tim="104815" ftm="108.26"/>
<marker lat="40.22030" lng="-110.03338" phz="Descent" hgt=" 17099" tim="104831" ftm="108.52"/>
<marker lat="40.22030" lng="-110.03380" phz="Descent" hgt=" 16523" tim="104845" ftm="108.75"/>
<marker lat="40.22029" lng="-110.03423" phz="Descent" hgt=" 15948" tim="104858" ftm="108.98"/>
<marker lat="40.22028" lng="-110.03466" phz="Descent" hgt=" 15372" tim="104912" ftm="109.21"/>
<marker lat="40.22028" lng="-110.03513" phz="Descent" hgt=" 14796" tim="104927" ftm="109.46"/>
<marker lat="40.22015" lng="-110.03567" phz="Descent" hgt=" 14255" tim="104940" ftm="109.68"/>
<marker lat="40.22002" lng="-110.03623" phz="Descent" hgt=" 13713" tim="104954" ftm="109.91"/>
<marker lat="40.21990" lng="-110.03679" phz="Descent" hgt=" 13172" tim="105008" ftm="110.14"/>
<marker lat="40.21976" lng="-110.03739" phz="Descent" hgt=" 12631" tim="105023" ftm="110.39"/>
<marker lat="40.21959" lng="-110.03788" phz="Descent" hgt=" 12118" tim="105036" ftm="110.61"/>
<marker lat="40.21942" lng="-110.03838" phz="Descent" hgt=" 11605" tim="105050" ftm="110.84"/>
<marker lat="40.21925" lng="-110.03888" phz="Descent" hgt=" 11093" tim="105104" ftm="111.07"/>
<marker lat="40.21907" lng="-110.03941" phz="Descent" hgt=" 10580" tim="105118" ftm="111.31"/>
<marker lat="40.21884" lng="-110.03960" phz="Descent" hgt=" 10094" tim="105131" ftm="111.53"/>
<marker lat="40.21860" lng="-110.03979" phz="Descent" hgt=" 9607" tim="105145" ftm="111.76"/>
<marker lat="40.21836" lng="-110.03999" phz="Descent" hgt=" 9121" tim="105159" ftm="111.99"/>
<marker lat="40.21811" lng="-110.04020" phz="Descent" hgt=" 8635" tim="105213" ftm="112.23"/>
<marker lat="40.21789" lng="-110.04005" phz="Descent" hgt=" 8175" tim="105227" ftm="112.45"/>
<marker lat="40.21766" lng="-110.03990" phz="Descent" hgt=" 7714" tim="105240" ftm="112.67"/>
<marker lat="40.21744" lng="-110.03976" phz="Descent" hgt=" 7254" tim="105253" ftm="112.89"/>
<marker lat="40.21720" lng="-110.03960" phz="Descent" hgt=" 6794" tim="105307" ftm="113.12"/>
<marker lat="40.21509" lng="-110.03690" phz="Touchdown" hgt=" 6679" tim="105633" ftm="116.55"/>"""

newarray1 = newdata.split("\n")
newarray2 = []
for marker in newarray1:
    newarray2.append(marker.split('"'))

for marker in newarray2:
    writetoKML.writeonce("%s,%s,%s" % (marker[3],marker[1],marker[7].strip(" ")),"./NSV.kml")
