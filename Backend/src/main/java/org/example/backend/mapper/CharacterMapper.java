package org.example.backend.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.example.backend.pojo.Character;

import java.util.List;

@Mapper
public interface CharacterMapper {
    List<Character> getCharacter(String name);

    String getBackground(int id);

    int insertSaveCharacter(String username, int characterId);

    Character getCharacterById(Integer characterId);
}
