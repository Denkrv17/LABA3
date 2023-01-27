import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True


def create_element(build_ele, doc):

    element = LABA3(doc)
    return element.create(build_ele)


class LABA3:


    def __init__(self, doc):

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_ele):

        self.connect_all_parts(build_ele)
        self.create_down_part_LABA3(build_ele)
        return (self.model_ele_list, self.handle_list)

    def connect_all_parts(self, build_ele):

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = 3
        com_prop.Stroke = 1
        circle_bottom = self.create_down_part_LABA3(build_ele)
        circle_center = self.create_central_part_LABA3(build_ele)
        circle_top = self.create_top_part_LABA3(build_ele)
        err, circle = AllplanGeo.MakeUnion(circle_bottom, circle_center)
        if err:
            return

        err, circle = AllplanGeo.MakeUnion(circle, circle_top)
        if err:
            return 

        self.model_ele_list.append(
            AllplanBasisElements.ModelElement3D(com_prop, circle))

    # must be updated
    def create_down_part_LABA3(self, build_ele):

        circle = self.down_part_addi_1(build_ele)
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_3(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_4(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_2_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_3_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_4_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_2_3(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_3_3(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_2_4(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.down_part_addi_3_4(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.last_down_part(build_ele))
        return circle

    def create_central_part_LABA3(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value, 
                                        build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 
                                        build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - (build_ele.CenterWidLength.value + build_ele.TransitLength.value), 
                                        build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 
                                        build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value,
                                         build_ele.BottomWid.value - build_ele.CutBottLength.value, 
                                         build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value,
                                        build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 
                                        build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value,
                                        build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 
                                        build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value,
                                        build_ele.CutBottLength.value, 
                                        build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(0, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        if err:
            return []

        return circle

    def create_top_part_LABA3(self, build_ele):

        circle = self.top_part_addi_1(build_ele)
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_3(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_3(build_ele, plus=(build_ele.Length.value - build_ele.CenterWidLength.value)))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_4(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_2_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_4(build_ele, build_ele.BottomWid.value - build_ele.CutBottLength.value * 2, build_ele.TopWid.value, 10))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_2_3(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_4_2(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_4_2(build_ele, build_ele.BottomWid.value - build_ele.CutBottLength.value * 2, build_ele.TopWid.value, 10))
        err, circle = AllplanGeo.MakeUnion(circle, self.top_part_addi_3_3(build_ele))
        err, circle = AllplanGeo.MakeUnion(circle, self.last_top_part(build_ele))
        return circle

    def top_part_addi_1(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                        build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                        build_ele.TopWid.value - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                        -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                        build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                        build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                        build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, 
                                        build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2,
                                        build_ele.BottHei.value + build_ele.CenterHei.value)
        
        err, circle = AllplanGeo.Createcircle(base_pol, path)

        if err:
            return []

        return circle

    def top_part_addi_2(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 , build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 , build_ele.BottomWid.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value + 10, build_ele.BottomWid.value - build_ele.CutBottLength.value - 10, build_ele.BottHei.value + build_ele.CenterHei.value + 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def top_part_addi_3(self, build_ele, plus=0):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(plus, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(plus, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(plus, build_ele.BottomWid.value + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(plus, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(plus, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(plus, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(plus + build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def top_part_addi_4(self, build_ele, minus_1 = 0, minus_2 = 0, digit = -10):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.TopWid.value - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 - minus_2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 - minus_2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value + digit - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)
        print(base_pol)
        print(path)
        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def top_part_addi_2_2(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value, build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value + 10, build_ele.CutBottLength.value + 10, build_ele.BottHei.value + build_ele.CenterHei.value + 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def top_part_addi_2_3(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value - 10, build_ele.BottomWid.value - build_ele.CutBottLength.value - 10, build_ele.BottHei.value + build_ele.CenterHei.value - 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def top_part_addi_4_2(self, build_ele, minus_1 = 0, minus_2 = 0, digit = -10):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 - minus_2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value + (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 - minus_2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - minus_1 + digit, build_ele.BottHei.value + build_ele.CenterHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        if err:
            return []

        return circle

    def top_part_addi_3_3(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value, build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value + build_ele.CenterHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value - 10, build_ele.CutBottLength.value + 10, build_ele.BottHei.value + build_ele.CenterHei.value - 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def last_top_part(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.TopWid.value - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.TopWid.value - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTop.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.TopWid.value - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 - build_ele.Identat.value, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTop.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.TopWid.value - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 - build_ele.Identat.value, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTop.value + build_ele.PlateHei.value)
        base_pol += AllplanGeo.Point3D(0, - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 + build_ele.Identat.value, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTop.value + build_ele.PlateHei.value)
        base_pol += AllplanGeo.Point3D(0, - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2 + build_ele.Identat.value, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTop.value)
        base_pol += AllplanGeo.Point3D(0, - (build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTop.value)
        base_pol += AllplanGeo.Point3D(0, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        path += AllplanGeo.Point3D(build_ele.Length.value, -(build_ele.TopWid.value - build_ele.BottomWid.value) / 2, build_ele.BottHei.value + build_ele.CenterHei.value + build_ele.HeiTopCut.value)
        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_1(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                    build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2,
                                    build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 
                                    build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2 - build_ele.WidthTinyPart.value,
                                    build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        err, circle = AllplanGeo.Createcircle(base_pol, path)

        if err:
            return []

        return circle
    
    def down_part_addi_2(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value - 10 , build_ele.BottomWid.value - build_ele.CutBottLength.value - 10, build_ele.BottHei.value - 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle


    def down_part_addi_3(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(0, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_4(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - 10, build_ele.BottHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        if err:
            return []

        return circle

    def down_part_addi_2_2(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value, build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + build_ele.TransitLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value,build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value,build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value - 10 ,build_ele.CutBottLength.value + 10, build_ele.BottHei.value - 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_3_2(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_4_2(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.CenterWidLength.value, build_ele.CutBottLength.value + 10, build_ele.BottHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        if err:
            return []

        return circle

    def down_part_addi_2_3(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value + 10, build_ele.BottomWid.value - build_ele.CutBottLength.value - 10, build_ele.BottHei.value + 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_3_3(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.BottomWid.value - build_ele.CutBottLength.value - 10, build_ele.BottHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_2_4(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value, build_ele.CutBottLength.value + (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - build_ele.TransitLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - 10, build_ele.CutBottLength.value + 10, build_ele.BottHei.value - 10)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def down_part_addi_3_4(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value - (build_ele.BottomWid.value - build_ele.CutBottLength.value * 2 - build_ele.WidthTinyPart.value) / 2, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value, build_ele.BottHei.value)
        path += AllplanGeo.Point3D(build_ele.Length.value - build_ele.CenterWidLength.value, build_ele.CutBottLength.value + 10, build_ele.BottHei.value)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

    def last_down_part(self, build_ele):

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, 20, 0)
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value - 20, 0)
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value, 20)
        base_pol += AllplanGeo.Point3D(0, build_ele.BottomWid.value, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(0, 0, build_ele.BottHei.value - build_ele.CutBottHei.value)
        base_pol += AllplanGeo.Point3D(0, 0, 20)
        base_pol += AllplanGeo.Point3D(0, 20, 0)

        if not GeometryValidate.is_valid(base_pol):
            return

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 20, 0)
        path += AllplanGeo.Point3D(build_ele.Length.value,20,0)

        err, circle = AllplanGeo.Createcircle(base_pol, path)

        
        if err:
            return []

        return circle

