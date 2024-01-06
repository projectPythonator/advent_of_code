
from bisect import bisect_right

class Seed_Solver():
    def __init__(self):
        self.list_of_seed = []
        self.seeds = []
        self.soils = []
        self.ferts = []
        self.watrs = []
        self.lites = []
        self.temps = []
        self.humds = []
        self.seed_to_soil = {}
        self.soil_to_fert = {}
        self.fert_to_watr = {}
        self.watr_to_lite = {}
        self.lite_to_temp = {}
        self.temp_to_humd = {}
        self.humd_to_location = {}
        
    def read_set(self, listed, mapped):
        seto = set(list('sfwlth'))
        for line in self.stdin:
            lino = line.strip()
            if len(lino)==0:
                break
            if lino[0] in seto:
                continue
            dest, source, length = map(int, lino.split(' '))
            listed.append(source)
            mapped[source] = (dest, length)
        for k,v in mapped.items():
            if k+v[1] not in mapped:
                listed.append(k+v[1])
        if 0 not in mapped:
            listed.append(0)
        listed.sort()

    def find_le(self, listo, val):
        i = bisect_right(listo, val)
        if i:
            return listo[i-1]
    
    def get_next_val(self, mapper, list_val, base_val):
        if list_val not in mapper:
            return base_val
        r_val = mapper[list_val][0]
        return r_val+(base_val-list_val)
    
    def get_location_helper(self, listo, mapper, base_val):
        list_val = self.find_le(listo, base_val)
        return self.get_next_val(mapper, list_val, base_val)    

    def get_location(self, base_val):
        base_val = self.get_location_helper(self.seeds, self.seed_to_soil, base_val)
        base_val = self.get_location_helper(self.soils, self.soil_to_fert, base_val)
        base_val = self.get_location_helper(self.ferts, self.fert_to_watr, base_val)
        base_val = self.get_location_helper(self.watrs, self.watr_to_lite, base_val)
        base_val = self.get_location_helper(self.lites, self.lite_to_temp, base_val)
        base_val = self.get_location_helper(self.temps, self.temp_to_humd, base_val)
        base_val = self.get_location_helper(self.humds, self.humd_to_location, base_val)
        return base_val

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        line = self.stdin.readline().strip()
        line = line[7:] #7 used because "seeds: " is 7 chars
        self.list_of_seed = map(int, line.split(' '))
        line = self.stdin.readline().strip()
        self.read_set(self.seeds, self.seed_to_soil)
        self.read_set(self.soils, self.soil_to_fert)
        self.read_set(self.ferts, self.fert_to_watr)
        self.read_set(self.watrs, self.watr_to_lite)
        self.read_set(self.lites, self.lite_to_temp)
        self.read_set(self.temps, self.temp_to_humd)
        self.read_set(self.humds, self.humd_to_location)
        self.stdin.close()
        
    def solve_seeder(self):
        ans = 10**63
        for el in self.list_of_seed:
            ans = min(ans, self.get_location(el))
        print(ans)


def main():
    print("hellow world")
    obj = Seed_Solver()
    obj.read_inputs()
    obj.solve_seeder()
main()
    
    
    
    