package org.example.backend.service;

import org.apache.el.parser.Token;
import org.example.backend.pojo.*;
import org.springframework.stereotype.Service;


public interface LoginService {
    LoginResult login(LoginPo po);

    LoginResult register(RegisterPo po);

    guestResult guest();
}
