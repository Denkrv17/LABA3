import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


def check_allplan_version(sozd_element, version):
    del sozd_element
    del version
    return True


def create_element(sozd_element, doc):

    element = LABA3(doc)
    return element.create(sozd_element)


class LABA3:


    def __init__(self, doc):

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, sozd_element):

        self.build_pr_wchasts(sozd_element)
        self.create_nizhnya_chast_LABA3(sozd_element)
        return (self.model_ele_list, self.handle_list)

    def build_pr_wchasts(self, sozd_element):

        commad_propertis = AllplanBaseElements.CommonProperties()
        commad_propertis.GetGlobalProperties()
        commad_propertis.Pen = 1
        commad_propertis.Color = 3
        commad_propertis.Stroke = 1
        kolo_bottom = self.create_nizhnya_chast_LABA3(sozd_element)
        kolo_center = self.create_central_chast_LABA3(sozd_element)
        kolo_vehniy = self.create_vehniy_chast_LABA3(sozd_element)
        pomylka, kolo = AllplanGeo.MakeUnion(kolo_bottom, kolo_center)
        if pomylka:
            return

        pomylka, kolo = AllplanGeo.MakeUnion(kolo, kolo_vehniy)
        if pomylka:
            return 

        self.model_ele_list.append(
            AllplanBasisElements.ModelElement3D(commad_propertis, kolo))

    
    def create_nizhnya_chast_LABA3(self, sozd_element):

        kolo = self.nizhnya_chast_addi_1(sozd_element)
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_3(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_4(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_2_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_3_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_4_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_2_3(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_3_3(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_2_4(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.nizhnya_chast_addi_3_4(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.ost_nizhnya_chast(sozd_element))
        return kolo

    def create_central_chast_LABA3(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2,sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - (sozd_element.CenterWidLength.value + sozd_element.TransitLength.value),sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value,sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value,sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value, sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2,sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value,sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathernern = AllplanGeo.Polyline3D()
        pathernern += AllplanGeo.Point3D(0, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathernern += AllplanGeo.Point3D(0, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathernern)

        if pomylka:
            return []

        return kolo

    def create_vehniy_chast_LABA3(self, sozd_element):

        kolo = self.vehniy_chast_addi_1(sozd_element)
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_3(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_3(sozd_element, plus=(sozd_element.Length.value - sozd_element.CenterWidLength.value)))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_4(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_2_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_4(sozd_element, sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2, sozd_element.vehniyWid.value, 10))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_2_3(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_4_2(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_4_2(sozd_element, sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2, sozd_element.vehniyWid.value, 10))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.vehniy_chast_addi_3_3(sozd_element))
        pomylka, kolo = AllplanGeo.MakeUnion(kolo, self.last_vehniy_chast(sozd_element))
        return kolo

    def vehniy_chast_addi_1(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.vehniyWid.value - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value,(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2,sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2,sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2,sozd_element.BottHei.value + sozd_element.CenterHei.value)
        
        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2,sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value,  sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2,  sozd_element.BottHei.value + sozd_element.CenterHei.value)
        
        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_2(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 , sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 , sozd_element.BottomWid.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value + 10, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - 10, sozd_element.BottHei.value + sozd_element.CenterHei.value + 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_3(self, sozd_element, plus=0):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(plus, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(plus, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(plus, sozd_element.BottomWid.value + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(plus, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(plus, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)

        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(plus, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(plus + sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_4(self, sozd_element, minus_1 = 0, minus_2 = 0, digit = -10):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.vehniyWid.value - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 - minus_2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 - minus_2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value + digit - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        print(basepoligon3D)
        print(pathern)
        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_2_2(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value, sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value + 10, sozd_element.CutBottLength.value + 10, sozd_element.BottHei.value + sozd_element.CenterHei.value + 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_2_3(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value - 10, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - 10, sozd_element.BottHei.value + sozd_element.CenterHei.value - 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_4_2(self, sozd_element, minus_1 = 0, minus_2 = 0, digit = -10):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 - minus_2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value + (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 - minus_2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        
        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - minus_1 + digit, sozd_element.BottHei.value + sozd_element.CenterHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        if pomylka:
            return []

        return kolo

    def vehniy_chast_addi_3_3(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value, sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value + sozd_element.CenterHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value - 10, sozd_element.CutBottLength.value + 10, sozd_element.BottHei.value + sozd_element.CenterHei.value - 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def last_vehniy_chast(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(0, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.vehniyWid.value - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.vehniyWid.value - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.Heivehniy.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.vehniyWid.value - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 - sozd_element.Identat.value, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.Heivehniy.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.vehniyWid.value - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 - sozd_element.Identat.value, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.Heivehniy.value + sozd_element.PlateHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 + sozd_element.Identat.value, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.Heivehniy.value + sozd_element.PlateHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2 + sozd_element.Identat.value, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.Heivehniy.value)
        basepoligon3D += AllplanGeo.Point3D(0, - (sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.Heivehniy.value)
        basepoligon3D += AllplanGeo.Point3D(0, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)

        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(0, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value, -(sozd_element.vehniyWid.value - sozd_element.BottomWid.value) / 2, sozd_element.BottHei.value + sozd_element.CenterHei.value + sozd_element.HeivehniyCut.value)
        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_1(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value,  sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value,  sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2 - sozd_element.WidthTinychast.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)

        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        if pomylka:
            return []

        return kolo
    
    def nizhniy_chast_addi_2(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value - 10 , sozd_element.BottomWid.value - sozd_element.CutBottLength.value - 10, sozd_element.BottHei.value - 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo


    def nizhniy_chast_addi_3(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)

        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(0, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_4(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        
        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - 10, sozd_element.BottHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_2_2(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value, sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + sozd_element.TransitLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value,sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value,sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value - 10 ,sozd_element.CutBottLength.value + 10, sozd_element.BottHei.value - 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_3_2(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)

        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_4_2(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        
        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value + 10, sozd_element.BottHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_2_3(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value + 10, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - 10, sozd_element.BottHei.value + 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_3_3(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.BottomWid.value - sozd_element.CutBottLength.value - 10, sozd_element.BottHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_2_4(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value, sozd_element.CutBottLength.value + (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - sozd_element.TransitLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - 10, sozd_element.CutBottLength.value + 10, sozd_element.BottHei.value - 10)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def nizhniy_chast_addi_3_4(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value - (sozd_element.BottomWid.value - sozd_element.CutBottLength.value * 2 - sozd_element.WidthTinychast.value) / 2, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)


        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value, sozd_element.BottHei.value)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value - sozd_element.CenterWidLength.value, sozd_element.CutBottLength.value + 10, sozd_element.BottHei.value)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

    def ost_nizhnya_chast(self, sozd_element):

        basepoligon3D = AllplanGeo.Polygon3D()
        basepoligon3D += AllplanGeo.Point3D(0, 20, 0)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value - 20, 0)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value, 20)
        basepoligon3D += AllplanGeo.Point3D(0, sozd_element.BottomWid.value, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, 0, sozd_element.BottHei.value - sozd_element.CutBottHei.value)
        basepoligon3D += AllplanGeo.Point3D(0, 0, 20)
        basepoligon3D += AllplanGeo.Point3D(0, 20, 0)

        if not GeometryValidate.is_valid(basepoligon3D):
            return

        pathern = AllplanGeo.Polyline3D()
        pathern += AllplanGeo.Point3D(0, 20, 0)
        pathern += AllplanGeo.Point3D(sozd_element.Length.value,20,0)

        pomylka, kolo = AllplanGeo.Createkolo(basepoligon3D, pathern)

        
        if pomylka:
            return []

        return kolo

