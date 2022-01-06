function verlet(pos::Float64, acc::Float64, dt::Float64)
    prev_pos = pos
    time = 0.0

    while (pos > 0)
        time += dt
        temp_pos = pos
        pos = pos * 2 - prev_pos + acc * dt * dt
        prev_pos = temp_pos
    end

    return time
end