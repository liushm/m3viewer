#!/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from PIL import Image

import os
import sys
import time
import math
import ctypes
import random

import mesh

program = None
locMVM = None
locPrM = None
locTex = None
meshes = []
texmap = {}
frames = 0
lasttime = time.time()

vs = open('shaders/vs.glsl').read() if os.path.isfile('shaders/vs.glsl') else open('c:/users/terran/documents/workspace/m3viewer/shaders/vs.glsl').read()
fs = open('shaders/fs.glsl').read() if os.path.isfile('shaders/fs.glsl') else open('c:/users/terran/documents/workspace/m3viewer/shaders/fs.glsl').read()

def InitShader():
    global program, locMVM, locPrM, locTex
    program = compileProgram(compileShader(vs, GL_VERTEX_SHADER), compileShader(fs, GL_FRAGMENT_SHADER))
    locMVM = glGetUniformLocation(program, 'modelViewMatrix')
    locPrM = glGetUniformLocation(program, 'projectionMatrix')
    locTex = glGetUniformLocation(program, 'texture0')

def InitBuffer():
    for obj in mesh.gl_objects:
        xyzs, normals, uvs, faces, mat = obj[0], obj[1], obj[2], obj[3], obj[4]

        vbo = glGenBuffers(3)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
        glBufferData(GL_ARRAY_BUFFER, 4 * len(xyzs), (ctypes.c_float*len(xyzs))(*xyzs), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
        glBufferData(GL_ARRAY_BUFFER, 4 * len(normals), (ctypes.c_float*len(normals))(*normals), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
        glBufferData(GL_ARRAY_BUFFER, 4 * len(uvs), (ctypes.c_float*len(uvs))(*uvs), GL_STATIC_DRAW)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)

        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 2 * len(faces), (ctypes.c_short*len(faces))(*faces), GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        meshes.append((vao, ibo, mat, len(faces)))
        print 'vao, ibo, mat, len', (vao, ibo, mat, len(faces))

def LoadTexture(filename):
    basename = os.path.basename(filename)

    if not os.path.isfile(filename):
        filename = basename
    if not os.path.isfile(filename):
        filename = './texture/' + basename
    if not os.path.isfile(filename):
        filename = 'd:/assets/mods/heroes.stormmod/base.stormassets/assets/textures/' + basename

    try:
        image = Image.open(filename)
    except:
        print 'warning: texture {} not found!'.format(basename)
        image = Image.new('RGBA', (256, 256), '#ffffff')

    return image

def InitTexture():
    glActiveTexture(GL_TEXTURE0)

    textnum = len(mesh.gl_texture)
    if (textnum <= 0):
        return

    texture = glGenTextures(textnum)
    if textnum == 1:
        texture = [texture]

    for i in xrange(textnum):
        filename = mesh.gl_texture[i]

        texmap[i] = texture[i]

        image = LoadTexture(filename)

        glBindTexture(GL_TEXTURE_2D, texture[i])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image.tobytes())

def InitGL(width,height):
    glClearColor(0.5, 0.5, 0.5, 0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)
    InitShader()
    InitBuffer()
    InitTexture()

def DrawGLSceneWithVertexBuffer():
    for i in meshes:
        # [(vao, ibo, tex, len)]
        glBindVertexArray(i[0])
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, i[1])
        glBindTexture(GL_TEXTURE_2D, texmap[i[2]])
        glDrawElements(GL_TRIANGLES, i[3], GL_UNSIGNED_SHORT, None)

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    global frames, lasttime
    frames += 1
    ctm = time.time()
    if ctm - lasttime >= 1.0:
        lasttime = ctm
        glutSetWindowTitle('opengl fps: %d' % frames)
        frames = 0

    glRotatef(30 * time.time() % 360.0, 0, 1.0, 0.0)

    glUseProgram(program)
    assert locMVM >= 0
    assert locPrM >= 0
    assert locTex >= 0
    glUniform1i(locTex, 0)

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    for i in xrange(100):
        glUniformMatrix4fv(locMVM, 1, GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX))
        glUniformMatrix4fv(locPrM, 1, GL_FALSE, glGetFloatv(GL_PROJECTION_MATRIX))

        DrawGLSceneWithVertexBuffer()
        glTranslatef(2.0, 0.0, 0.0)


    glutSwapBuffers()

def MouseButton(button, mode, x, y):
    # print 'clicked at', button, mode, time.time()
    if button == 3 and mode == GLUT_DOWN:
        glMatrixMode(GL_PROJECTION)
        glScalef(1.1, 1.1, 1.1)
    elif button == 4 and mode == GLUT_DOWN:
        glMatrixMode(GL_PROJECTION)
        glScalef(1/1.1, 1/1.1, 1/1.1)
    pass

def MouseMove(x, y):
    # print x, y
    pass

def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(-2, 2, -2, 2)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    gluLookAt(2, 1, 2, 0, 1, 0, 0, 1, 0)

def main():
    w, h = 800, 450

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(400, 300)
    glutCreateWindow("opengl")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutMouseFunc(MouseButton)
    glutMotionFunc(MouseMove)
    #glutPassiveMotionFunc(MouseMove)

    InitGL(w, h)

    glutMainLoop()

def install():
    import _winreg

    _winreg.SetValue(_winreg.HKEY_CLASSES_ROOT, r'.m3', _winreg.REG_SZ, 'm3file')
    _winreg.SetValue(_winreg.HKEY_CLASSES_ROOT, r'm3file\Shell\Open\command', _winreg.REG_SZ, r'"C:\Python27\python.exe" "C:\Users\terran\Documents\Workspace\m3viewer\main.py" "%1"')
    _winreg.SetValue(_winreg.HKEY_CLASSES_ROOT, r'm3file\DefaultIcon', _winreg.REG_SZ, '"%1"')

if __name__ == '__main__':
    print 'GL HF'

    # m3file = 'Storm_Hero_Ana_Base.m3'
    # m3file = 'Storm_Hero_Chen_Base.m3'
    # m3file = 'Storm_Hero_D3BarbarianF_Base.m3'
    # m3file = 'Storm_Hero_DVA_Base.m3'
    # m3file = 'Storm_Hero_Genji_Base.m3'
    # m3file = 'Storm_Hero_Jaina_Base.m3'
    # m3file = 'Storm_Hero_Junkrat_Base.m3'
    # m3file = 'Storm_Hero_Ragnaros_Base.m3'
    m3file = 'Storm_Hero_Medic_Base.m3'

    if len(sys.argv) == 2:
        m3file = sys.argv[1]

    mesh.load_mesh(m3file)
    main()
