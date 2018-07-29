
from m3addons import m3

obj_mat_map = {}

gl_texture = []
gl_objects = []

def load_mesh(filename):
    model = m3.loadModel(filename)

    # print hex(model.flags)
    print hex(model.vFlags)
    # print len(model.vertices)
    # print model.modelName
    # print model.divisions
    # print model.standardMaterials

    ##################################################################
    vertexClassName = "VertexFormat" + hex(model.vFlags)
    if not vertexClassName in m3.structures:
        raise Exception("Vertex flags %s can't behandled yet" % hex(model.vFlags))
    vertexStructureDescription = m3.structures[vertexClassName].getVersion(0)

    numberOfVertices = len(model.vertices) // vertexStructureDescription.size
    m3Vertices = vertexStructureDescription.createInstances(buffer=model.vertices, count=numberOfVertices)

    i = 0
    for mat in model.standardMaterials:
        print i, mat.name, mat.diffuseLayer[0].imagePath, mat.diffuseLayer[0].uvSource
        i += 1
        gl_texture.append(mat.diffuseLayer[0].imagePath)

    assert len(model.divisions) == 1
    division = model.divisions[0]
    # print division
    # print division.regions
    # print len(division.faces) // 3
    # print division.objects

    for obj in division.objects:
        obj_mat_map[obj.regionIndex] = obj.materialReferenceIndex
        print obj.regionIndex, '--->', obj.materialReferenceIndex

    for rid in xrange(len(division.regions)):
        region = division.regions[rid]
        vecs = m3Vertices[region.firstVertexIndex:region.firstVertexIndex + region.numberOfVertices]
        faces = division.faces[region.firstFaceVertexIndexIndex:region.firstFaceVertexIndexIndex + region.numberOfFaceVertexIndices]
        mat = model.standardMaterials[obj_mat_map[rid]]
        uvsrc = mat.diffuseLayer[0].uvSource
        texture = mat.diffuseLayer[0].imagePath
        xyzs = []
        normals = []
        uvs = []
        uvRatio = 2048.0 if (model.vFlags & 0xff) == 0x7d else 32768.0
        uvOffset = 0.0
        if hasattr(region, 'uvRatio') and hasattr(region, 'uvOffset'):
            uvRatio = uvRatio / region.uvRatio
            uvOffset = region.uvOffset
        uvcorrector = lambda uv: uv / uvRatio + uvOffset
        for v in vecs:
            x, y, z = v.position.x, v.position.y, v.position.z
            xyzs.append(x)
            xyzs.append(y)
            xyzs.append(z)
            nx, ny, nz = v.normal.x, v.normal.y, v.normal.z
            normals.append(nx)
            normals.append(ny)
            normals.append(nz)
            assert hasattr(v, 'uv{}'.format(uvsrc))
            uv = getattr(v, 'uv{}'.format(uvsrc))
            uvs.append(uvcorrector(uv.x))
            uvs.append(uvcorrector(uv.y))
        gl_objects.append((xyzs, normals, uvs, faces, obj_mat_map[rid]))

if __name__ == '__main__':
    # load_mesh('Storm_Hero_Ana_Base.m3')
    # load_mesh('Storm_Hero_Chen_Base.m3')
    # load_mesh('Storm_Hero_D3BarbarianF_Base.m3')
    # load_mesh('Storm_Hero_DVA_Base.m3')
    # load_mesh('Storm_Hero_Genji_Base.m3')
    # load_mesh('Storm_Hero_Jaina_Base.m3')
    # load_mesh('Storm_Hero_Junkrat_Base.m3')

    load_mesh('Storm_Hero_Ragnaros_Base.m3')
