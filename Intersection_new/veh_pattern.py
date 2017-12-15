# Vehicles Pattern1(from W to S)
        for i, veh in enumerate(self.vehicles_W_S):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
                # Make the room not available for other vehicles
                for j in range(11):
                    self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().x == 260:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t, self.sendData_1["vehicle"][i], 0):
                        veh.getPosition().x += veh.getSpeed().x
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_1)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))

                else:
                    # Already in the intersection
                    if 270 < veh.getPosition().x < 318 and veh.getPosition().y < 330:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.beze_t[i] / (318 - 270)), 2) * 270 + 2 * (self.beze_t[i] / (318 - 270)) * (
                        1 - self.beze_t[i] / (318 - 270)) * 318 + pow(
                            self.beze_t[i] / (318 - 270), 2) * 318
                        y = pow(1 - (self.beze_t[i] / (318 - 270)), 2) * 283 + 2 * (self.beze_t[i] / (318 - 270)) * (
                        1 - self.beze_t[i] / (318 - 270)) * 283 + pow(
                            self.beze_t[i] / (318 - 270), 2) * 320
                        veh.setPosition(Position(x, y))

                        self.beze_t[i] += 2

                        # Calculate rotation angle
                        qp.save()
                        qp.translate(veh.getPosition().x, veh.getPosition().y)

                        if ((veh.getPosition().x - 270 + veh.getSpeed().x) / (318 - 270)) * 90 > 15:
                            self.r[i] = ((veh.getPosition().x - 270 + veh.getSpeed().x) / (318 - 270)) * 90
                            qp.rotate(self.r[i])
                        elif ((veh.getPosition().x - 270 + veh.getSpeed().x) / (318 - 270)) * 90 > 90:
                            self.r[i] = 90
                            qp.rotate(self.r[i])
                        else:
                            self.r[i] = 0
                            qp.rotate(self.r[i])
                        qp.translate(-veh.getPosition().x, -veh.getPosition().y)
                        print('***************************************************')
                        print(i, veh.getPosition().x, veh.getPosition().y)

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        # for j in range(11):
                        #     self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
                        qp.restore()

                    # Already left intersection
                    elif 318 <= veh.getPosition().x and veh.getPosition().y < 600:

                        veh.getPosition().y += veh.getSpeed().x

                        qp.save()
                        qp.translate(veh.getPosition().x, veh.getPosition().y)
                        qp.rotate(90)
                        qp.translate(-veh.getPosition().x, -veh.getPosition().y)

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, sendData_1)

                        # print('***************************************************')
                        # print(veh.getPosition().x, veh.getPosition().y)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y - j))
                        qp.restore()

                    # Already left screen
                    elif veh.getPosition().y >= 600:
                        veh.getPosition().x = 0
                        veh.getPosition().y = 283
                        self.beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_1)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y - j))

                    # Move horizontal direction(across X_axis)
                    else:
                        veh.getPosition().x += veh.getSpeed().x
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_1)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))

# Vehicles Pattern2(from N to W)
for i, veh in enumerate(self.vehicles_N_W):
    # Check if there are vehicles ahead. If true, stop
    if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                              veh.getPosition().y, self.sendData_2)
        qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
        # Make the room not available for other vehicles
        for j in range(11):
            self.collision_check_N.append((veh.getPosition().x - j, veh.getPosition().y))
    # Move forward
    else:
        # Just before the intersection
        if veh.getPosition().y == 260:
            # Try to make a reservation
            if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t, self.sendData_2["vehicle"][i], 0):
                veh.getPosition().y += veh.getSpeed().y
                # Influential veh_num calculation
                old_x = veh.getPosition().x - veh.getSpeed().x
                old_y = veh.getPosition().y - veh.getSpeed().y
                self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                      self.sendData_2)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                for j in range(11):
                    self.collision_check_N.append((veh.getPosition().x - j, veh.getPosition().y))
            # Enter intersection
            else:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_2)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                for j in range(11):
                    self.collision_check_N.append((veh.getPosition().x - j, veh.getPosition().y))

        else:
            # Already in the intersection
            if 270 < veh.getPosition().x < 318 and veh.getPosition().y < 330:

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[i] / (318 - 270)), 2) * 270 + 2 * (self.beze_t[i] / (318 - 270)) * (
                    1 - self.beze_t[i] / (318 - 270)) * 318 + pow(
                    self.beze_t[i] / (318 - 270), 2) * 318
                y = pow(1 - (self.beze_t[i] / (318 - 270)), 2) * 283 + 2 * (self.beze_t[i] / (318 - 270)) * (
                    1 - self.beze_t[i] / (318 - 270)) * 283 + pow(
                    self.beze_t[i] / (318 - 270), 2) * 320
                veh.setPosition(Position(x, y))

                self.beze_t[i] += 2

                # Calculate rotation angle
                qp.save()
                qp.translate(veh.getPosition().x, veh.getPosition().y)

                if ((veh.getPosition().x - 270 + veh.getSpeed().x) / (318 - 270)) * 90 > 15:
                    self.r[i] = ((veh.getPosition().x - 270 + veh.getSpeed().x) / (318 - 270)) * 90
                    qp.rotate(self.r[i])
                elif ((veh.getPosition().x - 270 + veh.getSpeed().x) / (318 - 270)) * 90 > 90:
                    self.r[i] = 90
                    qp.rotate(self.r[i])
                else:
                    self.r[i] = 0
                    qp.rotate(self.r[i])
                qp.translate(-veh.getPosition().x, -veh.getPosition().y)
                print('***************************************************')
                print(i, veh.getPosition().x, veh.getPosition().y)

                # Influential veh_num calculation
                self.calculate_vehnum_inside(i, self.sendData_2)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                # for j in range(11):
                #     self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
                qp.restore()

            # Already left intersection
            elif 318 <= veh.getPosition().x and veh.getPosition().y < 600:

                veh.getPosition().y += veh.getSpeed().x

                qp.save()
                qp.translate(veh.getPosition().x, veh.getPosition().y)
                qp.rotate(90)
                qp.translate(-veh.getPosition().x, -veh.getPosition().y)

                # Influential veh_num calculation
                old_x = veh.getPosition().x
                old_y = veh.getPosition().y - veh.getSpeed().x
                self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, sendData_2)

                # print('***************************************************')
                # print(veh.getPosition().x, veh.getPosition().y)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                for j in range(11):
                    self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y - j))
                qp.restore()

            # Already left screen
            elif veh.getPosition().y >= 600:
                veh.getPosition().x = 0
                veh.getPosition().y = 283
                self.beze_t[i] = 2
                # Influential veh_num calculation
                old_x = veh.getPosition().x - veh.getSpeed().x
                old_y = veh.getPosition().y - veh.getSpeed().y
                self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_2)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                for j in range(11):
                    self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - j))

            # Move horizontal direction(across X_axis)
            else:
                veh.getPosition().x += veh.getSpeed().x
                # Influential veh_num calculation
                old_x = veh.getPosition().x - veh.getSpeed().x
                old_y = veh.getPosition().y - veh.getSpeed().y
                self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_2)
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                for j in range(11):
                    self.collision_check_N.append((veh.getPosition().x - j, veh.getPosition().y))
