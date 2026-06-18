"""
history_manager.py —— 历史记录管理模块
- 违规截图自动保存到 outputs/violations/
- 历史记录读取、筛选、统计
"""
import os
import cv2
import json
import numpy as np
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# 基础路径
PROJECT_ROOT = Path(__file__).parent.parent
VIOLATIONS_DIR = PROJECT_ROOT / "outputs" / "violations"
RECORDS_FILE = VIOLATIONS_DIR / "records.json"


def get_violations_dir() -> Path:
    """获取违规截图保存目录（自动创建）"""
    VIOLATIONS_DIR.mkdir(parents=True, exist_ok=True)
    return VIOLATIONS_DIR


def save_violation_screenshot(
    image: np.ndarray,
    detections: List[Dict],
    source: str = "图片检测"
) -> Optional[Dict]:
    """
    保存违规截图，返回记录信息。
    当检测到未佩戴安全帽时自动保存。

    Args:
        image: OpenCV BGR 图像
        detections: 检测结果列表
        source: 检测来源（图片/视频/摄像头/危险区域）

    Returns:
        记录字典（无违规时返回 None）
    """
    violations = [d for d in detections if d.get('class') == 'head' or d.get('class') == 'no_helmet']
    if not violations:
        return None

    # 在图片上画框
    annotated = image.copy()
    for det in detections:
        x1, y1, x2, y2 = [int(v) for v in det['bbox']]
        is_violation = det['class'] in ('head', 'no_helmet')
        color = (0, 0, 255) if is_violation else (0, 255, 0)
        label = f"NO Helmet {det['confidence']:.0%}" if is_violation else f"Helmet {det['confidence']:.0%}"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(annotated, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(annotated, label, (x1 + 2, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 生成文件名
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    vio_count = len(violations)

    # 只保存违规帧（含标注）
    vio_dir = get_violations_dir()
    filename = f"violation_{timestamp_str}_cam{source[:2]}_vio{vio_count}.jpg"
    filepath = vio_dir / filename
    cv2.imwrite(str(filepath), annotated)

    # 生成缩略图
    thumb_filename = f"thumb_{timestamp_str}.jpg"
    thumb_path = vio_dir / thumb_filename
    h, w = annotated.shape[:2]
    scale = min(300 / w, 200 / h)
    thumb = cv2.resize(annotated, (int(w * scale), int(h * scale)))
    cv2.imwrite(str(thumb_path), thumb)

    # 记录信息
    record = {
        "id": f"VIO-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}",
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "violation_count": vio_count,
        "total_detected": len(detections),
        "violation_rate": round(vio_count / max(len(detections), 1) * 100, 1),
        "image_path": str(filepath),
        "thumbnail_path": str(thumb_path),
        "status": "待处理"
    }

    # 追加到记录文件
    save_record(record)
    return record


def save_record(record: Dict):
    """将违规记录追加到 records.json"""
    records = load_all_records()
    records.insert(0, record)  # 最新在最前
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_all_records() -> List[Dict]:
    """加载所有违规记录"""
    if not RECORDS_FILE.exists():
        return []
    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def get_history_stats(records: List[Dict]) -> Dict:
    """获取历史记录统计信息"""
    total = len(records)
    handled = sum(1 for r in records if r.get("status") == "已处理")
    pending = total - handled
    total_violations = sum(r.get("violation_count", 0) for r in records)
    return {
        "total_records": total,
        "handled": handled,
        "pending": pending,
        "total_violations": total_violations,
        "handle_rate": round(handled / max(total, 1) * 100, 1)
    }


def filter_records(
    records: List[Dict],
    time_range: str = "全部",
    source: str = "全部",
    status: str = "全部",
    keyword: str = ""
) -> List[Dict]:
    """筛选违规记录"""
    filtered = records.copy()

    # 时间筛选
    if time_range != "全部":
        now = datetime.now()
        if time_range == "今日":
            cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == "近7天":
            cutoff = now - timedelta(days=7)
        elif time_range == "近30天":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = None

        if cutoff:
            filtered = [
                r for r in filtered
                if datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S") >= cutoff
            ]

    # 来源筛选
    if source != "全部":
        filtered = [r for r in filtered if r.get("source") == source]

    # 状态筛选
    if status != "全部":
        filtered = [r for r in filtered if r.get("status") == status]

    # 关键词搜索
    if keyword:
        filtered = [
            r for r in filtered
            if keyword.lower() in r.get("id", "").lower()
            or keyword.lower() in r.get("timestamp", "").lower()
            or keyword.lower() in r.get("source", "").lower()
        ]

    return filtered


def update_record_status(record_id: str, new_status: str) -> bool:
    """更新违规记录的处理状态"""
    records = load_all_records()
    for r in records:
        if r["id"] == record_id:
            r["status"] = new_status
            with open(RECORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return True
    return False


def delete_record(record_id: str) -> bool:
    """删除违规记录和对应的截图文件"""
    records = load_all_records()
    for i, r in enumerate(records):
        if r["id"] == record_id:
            # 删除图片文件
            img_path = r.get("image_path", "")
            thumb_path = r.get("thumbnail_path", "")
            if img_path and os.path.exists(img_path):
                os.remove(img_path)
            if thumb_path and os.path.exists(thumb_path):
                os.remove(thumb_path)
            # 从记录中移除
            records.pop(i)
            with open(RECORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return True
    return False


def clear_all_records() -> bool:
    """清除所有历史记录和截图"""
    try:
        if VIOLATIONS_DIR.exists():
            shutil.rmtree(str(VIOLATIONS_DIR))
        VIOLATIONS_DIR.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False