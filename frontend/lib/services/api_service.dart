import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Use 10.0.2.2 if testing on an Android emulator, or localhost for web/iOS
  static const String baseUrl = 'http://127.0.0.1:8000';

  // Fetch the active quests for a student
  Future<List<dynamic>> fetchQuests(int studentId) async {
    final response = await http.get(Uri.parse('$baseUrl/quests/$studentId'));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load quests. Server responded with: ${response.statusCode}');
    }
  }

  // Complete a quest and log XP
  Future<bool> completeQuest(int questId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/quests/$questId/complete'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
    );
    
    return response.statusCode == 200;
  }
}