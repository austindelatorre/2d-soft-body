class Body(object):
    pos = (0.0, 0.0)
    vel = (0.0, 0.0)
    acc = (0.0, 0.0)
    mass = 1.0
    drag = 0.1

    def update(dt):
        pos = pos + vel*dt + acc*(dt*dt*0.5)
        new_acc = apply_forces()
        vel = vel + (acc+new_acc)*(dt*0.5)

    def apply_forces():
        grav_acc = (0.0, -9.81)
        drag_force = 0.5 * drag * (vel * abs(vel))
        drag_acc = drag_force / mass
        return grav_acc - drag_acc;