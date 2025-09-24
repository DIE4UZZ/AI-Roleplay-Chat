package org.example.backend.service;

import org.apache.el.parser.Token;
import org.example.backend.pojo.LoginPo;
import org.example.backend.pojo.RegisterPo;
import org.example.backend.pojo.Result;
import org.springframework.stereotype.Service;


public interface LoginService {
    Result login(LoginPo po);

    Result register(RegisterPo po);
}
