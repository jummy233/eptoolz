

```python
from eptoolz.orm import EPObject
from eptoolz.type import Real, String, Name
from eptoolz import EnergyPlus

output = './John/Doe/'
env = '/home/John/Doe/Opt/EnergyPlus/'
idd = '.myidd.idd'
idf = '/John/Doe/myidf.idf'
epw = '../ShanghaiMinhang.epw'

env = EPEnv(env=env, idd=idd, idf=idf, epw=epw, output=output)
ep = EnergyPlus(env)

myidd = __import__('myidd.idd')
# substitute material object in a given idf

material1 = ep.Site.Material(
    name="A2 - 4 IN DENSE FACE BRICK",
    conductivity= 1.245296,
    density= 2082.4,
    roughness= Rough,
    solar_absorptance= 0.93,
    specific_heat= 920.48,
    thermal_absorptance= 0.9,
    thickness= 0.1014984,
    vsdisible_absorptance= 0.93
)
ep.idf["A2 - 4 IN DENSE FACE BRICK"] = material1

# modify one field in idf
ep.idf["A2 - 4 IN DENSE FACE BRICK"].density = 2020

# append object into idf
material2 = ep.Site.Material(
    name="A1 - 4 IN DENSE FACE BRICK",
    conductivity= 1.245296,
    density= 1082.4,
    roughness= Rough,
    solar_absorptance= 0.93,
    specific_heat= 92.48,
    thermal_absorptance= 0.9,
    thickness= 0.1014984,
    vsdisible_absorptance= 0.93
)
ep.idf.append(material2)

# output idf to another file
ep.idf.write('../idf2.idf')


```
