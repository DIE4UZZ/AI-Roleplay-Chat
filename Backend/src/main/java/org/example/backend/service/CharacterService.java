package org.example.backend.service;

import jakarta.servlet.http.HttpServletRequest;
import org.example.backend.pojo.Result;
import org.example.backend.pojo.getCharacterResult;

public interface CharacterService {

    getCharacterResult getCharacter(String keyword, int page, int size);

    Result getBackground(int id);

    Result saveCharacter(int roleId, HttpServletRequest request);

    Result getSaveCharacter(HttpServletRequest request);
}
