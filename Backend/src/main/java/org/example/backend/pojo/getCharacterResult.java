package org.example.backend.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class getCharacterResult {
    private int total;
    private List<Character> list;

    public static getCharacterResult success(List<Character> list) {
        return new getCharacterResult(1,list);
    }

    public static getCharacterResult error(){return new getCharacterResult(0, null);}
}
