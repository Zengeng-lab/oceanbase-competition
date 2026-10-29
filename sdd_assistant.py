import json
import os
from openai import OpenAI

# MiniMax API配置（把你的API Key填这里）
client = OpenAI(
    api_key="YOUR_MINIMAX_API_KEY",  # 替换成你自己的Key
    base_url="https://api.minimax.chat/v1"
)

# 模拟PowerContext：保存任务状态
STATE_FILE = "task_state.json"
# 模拟seekdb/OceanBase：存储代码上下文
CODE_STORE_FILE = "code_context.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"current_task": None, "completed_steps": []}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_code_context():
    if os.path.exists(CODE_STORE_FILE):
        with open(CODE_STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # 第一步：导入业务代码上下文
    with open("todo.py", "r", encoding="utf-8") as f:
        todo_code = f.read()
    context = {
        "business_code": todo_code,
        "requirements": "给TodoList增加删除指定索引任务的功能，方法名delete_task，参数task_index，删除后返回成功信息"
    }
    with open(CODE_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    return context

def modify_code_with_minimax(context):
    """用MiniMax完成实际代码修改"""
    prompt = f"""
    你是一个Python开发助手。根据下面的业务代码和需求，直接修改todo.py代码，增加删除任务的功能：
    
    当前业务代码：
    {context['business_code']}
    
    需要完成的修改：
    {context['requirements']}
    
    直接输出修改后的完整todo.py代码，不要解释。
    """
    
    response = client.chat.completions.create(
        model="abab6.5s-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    new_code = response.choices[0].message.content.strip()
    # 保存修改后的代码
    with open("todo.py", "w", encoding="utf-8") as f:
        f.write(new_code)
    return new_code

def run_tests():
    """跑测试验证代码修改"""
    import subprocess
    result = subprocess.run(["python", "test_todo.py"], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

if __name__ == "__main__":
    print("=== SDD开发助手启动 ===")
    
    # 1. 加载上下文和任务状态
    state = load_state()
    context = load_code_context()
    print("✅ 步骤1：导入业务代码与需求上下文完成")
    
    # 2. 执行代码修改
    state["current_task"] = "给TodoList增加delete_task功能"
    save_state(state)
    print("✅ 步骤2：任务状态已保存到PowerContext")
    
    # 3. 调用MiniMax修改代码
    print("🤖 调用MiniMax模型完成代码修改...")
    new_code = modify_code_with_minimax(context)
    state["completed_steps"].append("code_modified")
    save_state(state)
    print("✅ 步骤3：MiniMax完成代码修改")
    
    # 4. 跑测试验证
    print("🧪 运行测试验证修改结果...")
    test_pass = run_tests()
    if test_pass:
        state["completed_steps"].append("tests_passed")
        save_state(state)
        print("🎉 所有步骤完成！任务成功！")
    else:
        print("❌ 测试未通过")
    
    # 5. 模拟重新启动后读取状态
    print("\n=== 重启后读取任务状态 ===")
    loaded_state = load_state()
    print(f"已完成步骤：{loaded_state['completed_steps']}")
